import statsmodels.formula.api as smf
# import numpy as np
import plotly.express as px
import pandas as pd

def Average_Treatment_Effect(df, y_col, treatment_indices, control_indices):
    """
    Calculate Average Treatment Effect (ATE)
    @param df: pandas.DataFrame; the dataframe containing a column of treatment/control post-treatment values
    @param y_col: str; name of the column after treatment
    @param treatment_indices: list; list containing integers of all indices of data points that have been given treatment
    @param control_indices: list; list containing integers of all indices of data points that are control points
    @return: float; the calculated ATE
    """
    all_treatment_y = list(df.iloc[treatment_indices][y_col])
    all_control_y = list(df.iloc[control_indices][y_col])
    ATE = (sum(all_treatment_y)/len(all_treatment_y)) - (sum(all_control_y)/len(all_control_y))
    return ATE


def CUPED_csv(dir_, before_col, after_col, binary_col, show=False):
    """
    Uses CUPED function to read a CSV, create a new CSV with the new CUPED values as well as calculating ATE pre/post CUPED
    @param dir_: str; directory to CSV
    @param before_col: str; name of the column before treatment
    @param after_col: str; name of the column after treatment
    @param binary_col: str; name of column of 1s and 0s representing whether treatment has been given
    @param show: bool; default=True; if True then display distribution graphs of pre/post CUPED
    @return: floats; ATE before, ATE after, Variance before, Variance after
    """
    df = pd.read_csv(dir_)
    df2, ATE, ATE_CUPED, Variance, Variance_CUPED, percChangeReg, percChangeCUPED = CUPED(df, before_col, after_col, binary_col, show=show)
    df2.to_csv(dir_[:-4]+"_CUPED.csv")
    return ATE, ATE_CUPED, Variance, Variance_CUPED, percChangeReg, percChangeCUPED


def CUPED(df, before_col, after_col, binary_col, show=False):
    """
    Creates CUPED-modified data-frame from pandas DataFrame as well as plot the resulting distribution
    @param df: pandas.DataFrame; the dataframe
    @param before_col: str; name of the column before treatment
    @param after_col: str; name of the column after treatment
    @param binary_col: str; name of column of 1s and 0s representing whether treatment has been given
    @param show: bool; default=True; if True then display distribution graphs of pre/post CUPED
    @return: pandas.DataFrame, floats; CUPED processed DataFrame, ATE before, ATE after, Variance before, Variance after
    """
    # df[cuped_col] = df[after_col] - theta * (df[before_col] - np.mean(df[before_col]))  # CUPED column (deprecated)
    cuped_col = '{}_cuped'.format(after_col)  # cuped_col name
    expected_col = 'expected_{}'.format(after_col)

    # Theta
    theta = smf.ols('{} ~ {}'.format(after_col, before_col), data=df).fit().params[1]  # pre-CUPED theta

    # E[x] & Y_t bar data sets
    treatment_indices = df.index[df[binary_col] == 1].tolist()  # get index values of all binary = 1
    control_indices = df.index[df[binary_col] == 0].tolist()  # get index values of all binary = 0
    half = len(treatment_indices) // 2  # split the treatment into 2- one for E[x] and the other for Y_t bar
    expected_x_sample_indices = treatment_indices[:half]
    y_t_bar_sample_indices = treatment_indices[half:]
    expected_x_sample = list(df.iloc[expected_x_sample_indices][before_col])
    y_t_bar_sample = list(df.iloc[y_t_bar_sample_indices][after_col])


    # E[x] & Y_t bar
    expected_x = sum(expected_x_sample) / len(expected_x_sample)
    Y_t_bar = sum(y_t_bar_sample) / len(y_t_bar_sample)


    # X_t bar
    x_t_bar_sample = list(df.iloc[treatment_indices][before_col])
    x_t_bar = sum(x_t_bar_sample) / len(x_t_bar_sample)


    df[expected_col] = Y_t_bar - (theta * x_t_bar) + (theta * expected_x)  # expected column
    df[cuped_col] = abs(df[after_col] - df[expected_col])  # cuped column

    # theta_cuped = smf.ols("{} ~ {}".format(cuped_col, binary_col), data=df).fit().params[1]  # post-CUPED theta

    # display the distribution graphs
    if show:
        pre_cuped_fig = px.histogram(df, x=after_col, labels={after_col: "Pre-CUPED"}, color=binary_col)
        post_cuped_fig = px.histogram(df, x=cuped_col, labels={cuped_col: "Post-CUPED"}, color=binary_col)
        pre_cuped_fig.show()
        post_cuped_fig.show()

    variances = df.var()

    cuped_treatment_only = df.loc[df[binary_col] == 1, cuped_col]
    cuped_control_only = df.loc[df[binary_col] == 0, cuped_col]
    reg_treatment_only = df.loc[df[binary_col] == 1, after_col]
    reg_control_only = df.loc[df[binary_col] == 0, after_col]

    percChangeReg = (sum(reg_treatment_only) / sum(reg_control_only)) - 1
    percChangeCUPED = (sum(cuped_treatment_only) / sum(cuped_control_only)) - 1

    return df, Average_Treatment_Effect(df, after_col, treatment_indices, control_indices), Average_Treatment_Effect(df, cuped_col, treatment_indices, control_indices),\
        variances[after_col], variances[after_col+"_cuped"], percChangeReg, percChangeCUPED
