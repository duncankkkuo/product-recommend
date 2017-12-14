from sklearn.metrics.pairwise import pairwise_distances
import MySQLdb
import psycopg2
import pandas as pd
import numpy as np
import logging

def select_user(mysql_db):
    user_cursor = mysql_db.cursor()
    user_cursor.execute('SELECT user FROM view GROUP BY user HAVING (COUNT(user) > 20)')
    user_result = user_cursor.fetchall()
    user_list = []

    for user in user_result:
        user_list.append(user[0])

    logging.info("User count: " + str(len(user_list)))
    return user_list

def import_data(mysql_db, user_list):
    count = 0
    user_count = len(user_list)
    for user in user_list:
        count += 1
        if count%1000 == 0:
            userTuple= tuple(user_list[count-1000:count])
            sql = 'SELECT user, product_oid FROM view WHERE user IN' + str(userTuple)
            if count == 1000:
                df = pd.read_sql(sql, con=mysql_db)
            else:
                df_add = pd.read_sql(sql, con=mysql_db)
                df = pd.concat([df, df_add], ignore_index=True)
            logging.info("Data import with user count: " + str(count))

        elif count == user_count:
            userTuple= tuple(user_list[user_count-(count%1000)::])
            sql = 'SELECT user, product_oid FROM view WHERE user IN' + str(userTuple)
            df_add = pd.read_sql(sql, con=mysql_db)
            df = pd.concat([df, df_add], ignore_index=True)
            logging.info("Data import with user count: " + str(count))

    logging.info("Data count: " + str(len(df)))
    return df

def data_clean(df):
    df = df.drop_duplicates()
    df['rating'] = 1
    logging.info("Data clean finished")
    return df

def training(df):
    productRatings = df.pivot_table(index=['user'],columns=['product_oid'],values='rating',aggfunc=lambda x: len(x.unique()),fill_value=0)
    item_similarity = 1 - pairwise_distances(productRatings.T, metric = "cosine")
    product_ratings_pred = pd.DataFrame (
        data=item_similarity[:,:],
        index=productRatings.columns,
        columns=productRatings.columns
    )

    similar_products_pred = pd.DataFrame(index=product_ratings_pred.columns,columns=range(1,21))
    for i in range(0,len(product_ratings_pred.columns)):
        similar_products_pred.iloc[i,:20] = product_ratings_pred.iloc[0:,i].sort_values(ascending=False)[:20].index

    logging.info("Data training finished")
    return similar_products_pred, product_ratings_pred

def similar_products(similar_products_pred, product_ratings_pred, mysql_db, pg_db):
    product_cursor = pg_db.cursor()
    recommend_cursor = mysql_db.cursor()
    product_list = similar_products_pred.index.values.tolist()
    recommend_cursor.execute('DELETE FROM recommend')
    for prod_oid in product_list:
        similar_prod = similar_products_pred.loc[prod_oid].values.tolist()
        for similar_prod_oid in similar_prod:
            if similar_prod_oid != prod_oid:
                try:
                    product_cursor.execute("SELECT country_cd, city_cd FROM product_city WHERE prod_oid = %s", [similar_prod_oid])
                    result = product_cursor.fetchall()
                    recommend_cursor.execute('INSERT INTO recommend (prod_oid, similar_prod_oid, score, country_cd, city_cd) VALUES (%s,%s,%s,%s,%s)', (prod_oid, similar_prod_oid, product_ratings_pred.loc[prod_oid][similar_prod_oid], result[0][0], result[0][1]))
                except:
                    pass
        logging.info("Similar products predict finished: " + str(prod_oid))
    try:
        mysql_db.commit()
    except:
        mysql_db.rollback()

    logging.info("Similar products predict all finished")

def main():
    logging.basicConfig(
        level=logging.INFO,
        filename='~/recommend.log',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    mysql_db = MySQLdb.connect("localhost","user","password","recommend")
    pg_db = psycopg2.connect(database="kkdb", user="", password="", host="", port="5432")

    user_list = select_user(mysql_db)
    data = import_data(mysql_db, user_list)
    training_data = data_clean(data)
    similar_products_pred, product_ratings_pred = training(training_data)
    similar_products(similar_products_pred, product_ratings_pred, mysql_db, pg_db)

if __name__ == "__main__":
    main()
