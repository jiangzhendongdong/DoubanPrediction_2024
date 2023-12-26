import matplotlib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from pyinstrument import Profiler

profiler_get_detail = Profiler()
profiler_get_detail.start()


def data_preprocessing():
    movie = pd.read_csv("DoubanMoviesData.csv")

    threshold = 15
    columns_with_too_many_categories = []
    # 遍历DataFrame的列
    for column in movie.columns:
        # 计算每个列的唯一值数量
        unique_values_count = movie[column].nunique()
        # 如果唯一值数量超过阈值，则将该列添加到列表中
        if unique_values_count > threshold:
            columns_with_too_many_categories.append(column)

    # 非数值类型列
    non_numeric_columns = movie.select_dtypes(exclude=['number'])
    # 去掉无用的列
    df = movie.drop(columns=list(set(non_numeric_columns.columns) & set(columns_with_too_many_categories)))
    df['genres'] = movie['genres']

    # 缺失值填充
    # 类别类用null填充
    non_numeric_columns = df.select_dtypes(exclude=['number'])
    df[list(non_numeric_columns.columns)] = df[list(non_numeric_columns.columns)].fillna('null')
    # 数值用均值填充
    numeric_columns = [col for col in list(df.columns) if col not in list(non_numeric_columns.columns)]
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

    # 处理流派
    genres_dummies = df['genres'].str.get_dummies('|')
    df = pd.concat([df, genres_dummies], axis=1)

    matplotlib.rcParams['font.family'] = 'SimHei'

    # 对类别的列进行编码
    non_numeric_columns = df.select_dtypes(exclude=['number'])
    for fea in list(non_numeric_columns.columns):
        label_encoder = LabelEncoder()
        df[fea] = label_encoder.fit_transform(df[fea])

    x = df.drop(['douban_score'], axis=1)  # 特征
    y = df['douban_score']  # 目标变量

    return x, y


def split_train_test_data():
    x, y = data_preprocessing()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42, shuffle=True)
    return x_train, x_test, y_train, y_test


def get_prediction_result():
    x_train, x_test, y_train, y_test = split_train_test_data()
    rf_regressor = RandomForestRegressor(n_estimators=50, random_state=42)
    rf_regressor.fit(x_train, y_train)
    y_pred_rf = rf_regressor.predict(x_test)
    ratingscore = y_pred_rf[-1]
    return ratingscore


result = get_prediction_result()
print(result)

profiler_get_detail.stop()
profiler_get_detail.print()


def XXX():
    # x = df.drop(['douban_score'], axis=1)  # 特征
    # y = df['douban_score']  # 目标变量
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, shuffle=False)

    # dt_regressor = DecisionTreeRegressor(random_state=42)
    # dt_regressor.fit(x_train, y_train)
    # x_test['决策树模型预测评分'] = dt_regressor.predict(x_test)
    #
    # x = df.drop(['douban_score'], axis=1)  # 特征
    # y = df['douban_score']  # 目标变量
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, shuffle=False)
    #
    # lr_regressor = LinearRegression()
    # lr_regressor.fit(x_train, y_train)
    # x_test['线性回归模型预测评分'] = lr_regressor.predict(x_test)
    #
    # x = df.drop(['douban_score'], axis=1)  # 特征
    # y = df['douban_score']  # 目标变量
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, shuffle=False)
    #
    # xgb_regressor = XGBRegressor(random_state=42)
    # xgb_regressor.fit(x_train, y_train)
    # x_test['xgb_regressor模型预测评分'] = xgb_regressor.predict(x_test)
    #
    # x = df.drop(['douban_score'], axis=1)  # 特征
    # y = df['douban_score']  # 目标变量
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, shuffle=False)
    #
    # catboost_regressor = CatBoostRegressor(random_state=42, verbose=0)
    # catboost_regressor.fit(x_train, y_train)
    # x_test['catboost_regressor模型预测评分'] = catboost_regressor.predict(x_test)
    #
    # x = df.drop(['douban_score'], axis=1)  # 特征
    # y = df['douban_score']  # 目标变量
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, shuffle=False)
    #
    # lgbm_regressor = LGBMRegressor(random_state=42)
    # lgbm_regressor.fit(x_train, y_train)
    # x_test['lgbm_regressor模型预测评分'] = lgbm_regressor.predict(x_test)
    #
    # x = df.drop(['douban_score'], axis=1)  # 特征
    # y = df['douban_score']  # 目标变量
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # 训练各个回归模型

    # rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    # rf_regressor.fit(x_train, y_train)

    # dt_regressor = DecisionTreeRegressor(random_state=42)
    # dt_regressor.fit(x_train, y_train)
    #
    # lr_regressor = LinearRegression()
    # lr_regressor.fit(x_train, y_train)

    # xgb_regressor = xGBRegressor(random_state=42)
    # xgb_regressor.fit(x_train, y_train)

    # catboost_regressor = CatBoostRegressor(random_state=42, verbose=0)
    # catboost_regressor.fit(x_train, y_train)

    # lgbm_regressor = LGBMRegressor(random_state=42)
    # lgbm_regressor.fit(x_train, y_train)

    # 进行预测
    # y_pred_dt = dt_regressor.predict(x_test)
    # y_pred_lr = lr_regressor.predict(x_test)
    # y_pred_xgb = xgb_regressor.predict(x_test)
    # y_pred_catboost = catboost_regressor.predict(x_test)
    # y_pred_lgbm = lgbm_regressor.predict(x_test)

    # 计算各个模型的性能指标
    def evaluate_model(y_true, y_pred):
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        return mse, rmse, mae, r2

    # mse_rf, rmse_rf, mae_rf, r2_rf = evaluate_model(y_test, y_pred_rf)
    # mse_dt, rmse_dt, mae_dt, r2_dt = evaluate_model(y_test, y_pred_dt)
    # mse_lr, rmse_lr, mae_lr, r2_lr = evaluate_model(y_test, y_pred_lr)
    # mse_xgb, rmse_xgb, mae_xgb, r2_xgb = evaluate_model(y_test, y_pred_xgb)
    # mse_catboost, rmse_catboost, mae_catboost, r2_catboost = evaluate_model(y_test, y_pred_catboost)
    # mse_lgbm, rmse_lgbm, mae_lgbm, r2_lgbm = evaluate_model(y_test, y_pred_lgbm)

    # 创建数据框来比较各个模型的性能

    # comparison_df = pd.DataFrame({'Model': ['Random Forest', 'Decision Tree', 'Linear Regression', 'CatBoost'],
    #                               'MSE': [mse_rf, mse_dt, mse_lr, mse_catboost],
    #                               'RMSE': [rmse_rf, rmse_dt, rmse_lr, rmse_catboost],
    #                               'MAE': [mae_rf, mae_dt, mae_lr, mae_catboost],
    #                               'R^2': [r2_rf, r2_dt, r2_lr, r2_catboost]})
    #
    # predictions_df = pd.DataFrame({'True Values': y_test,
    #                                'Random Forest Predictions': y_pred_rf,
    #                                'Decision Tree Predictions': y_pred_dt,
    #                                'Linear Regression Predictions': y_pred_lr,
    #                                #                                'xGBoost Predictions': y_pred_xgb,
    #                                'CatBoost Predictions': y_pred_catboost, })
    #                                'LightGBM Predictions': y_pred_lgbm

    result = 1
    return result
