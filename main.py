import pandas as pd
import pytest
from evidently import ColumnMapping
from evidently.test_suite import TestSuite
from evidently.descriptors import *
from evidently.tests import *

def similiarity(df, display_name1, with_column1, on_column1):
    test_suite = TestSuite(tests=[
        TestColumnValueMin(
            column_name=SemanticSimilarity(
            display_name=display_name1,
            with_column=with_column1).
            on(on_column1),
            gte=0.9),
    ])
    print("created test suite object")
    test_suite.run(reference_data=None,current_data=df)
    print(test_suite.datasets().current)
    df1 = pd.DataFrame(test_suite.datasets().current)
    return df1

def regression_result(predicted_file_path, gold_file_path, columns1):
    predicted_df=pd.read_csv(predicted_file_path)
    print("pred", predicted_df.head())
    gold_df=pd.read_csv(gold_file_path)

    ## add _pred to predicted_df columns and merge both the dataframe, added new columns
    predicted_df1 = predicted_df[columns1]
    gold_df_selected = gold_df[columns1]

    # Add '_pred' to predicted_df columns
    predicted_df_selected = predicted_df1[columns1].rename(columns={col: col + '_pred' for col in columns1})

    # Merge the gold_df with the selected and renamed columns of predicted_df
    merge_df = pd.merge(gold_df_selected, predicted_df_selected, left_index=True, right_index=True)
    print("merge_df", merge_df.head(5))
    for i in columns1:
        print("i", i)
        
        display_name1=i+"_similiarity_score"
        with_column1=i 
        on_column=i+"_pred"

        print("display name", display_name1)
        print("with column", with_column1)
        print("on_columns", on_column)
        current_test_df=similiarity(merge_df,display_name1,with_column1,on_column)
        merge_df=current_test_df
    print(merge_df.columns)
    return merge_df

def test_score():
    generated_file=r'testing_workflow/file_sim_scores_detailed_01272025boilerplate.csv'
    gold_file=r'testing_workflow/file_sim_scores_detailed_01272025boilerplate1.csv'
    # Replace with the path to your gold file
    test_result=regression_result(generated_file, gold_file,["source_text_interpretation","most_similar_text","target_text_segment_most_common_interpretation","justification"])
    #"source_text_missing_in_target","reason_source_text_missing_in_target"
    test_result.to_csv("test_result.csv",index=False)
    #test_score(test_result)
    test_df=test_result
    ss=["source_text_interpretation_similiarity_score","most_similar_text_similiarity_score","target_text_segment_most_common_interpretation_similiarity_score","justification_similiarity_score"]
    #
    test_result_status=[]
    for i in ss:
        if (test_df[i] <0.9).any():
            test_result_status.append("False")
        else:
            test_result_status.append("True")

        #filtered_df = df[df[i] < 0.9]
    for status in test_result_status:
        assert status == "True", f"Test failed with status: {status}"








