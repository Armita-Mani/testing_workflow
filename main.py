import pandas as pd 
from evidently import ColumnMapping
from evidently.test_suite import TestSuite
from evidently.descriptors import *
from evidently.tests import *


data = [
    ["Hi there, how do I reset my password?", "To reset your password, click on 'Forgot Password' on the login page and follow the instructions sent to your registered email.", "To change your password, select 'Forgot Password' on the login screen and follow the steps sent to your registered email address."],
    ["Where can I find my transaction history?", "You can view your transaction history by logging into your account and navigating to the 'Transaction History' section.", "Log into your account and go to 'Transaction History' to see all your past transactions."],
    ["How do I add another user to my account?", "I am afraid it is not currently possible to add multiple users to the account.", "To add a secondary user, go to 'Account Settings', select 'Manage Users', and enter the details of the person you want to add. You can set permissions for their access."],
    ["Is it possible to link multiple bank accounts?", "Yes, you can link multiple bank accounts by going to 'Account Settings' and selecting 'Add Bank Account'.", "You can add multiple bank accounts by visiting 'Account Settings' and choosing 'Add Bank Account'."],
    ["Can I use your service for cryptocurrency transactions?", "Currently, our service does not support cryptocurrency transactions. Please check our website for updates regarding this feature.", "At the moment, cryptocurrency transactions are not supported by our service. Keep an eye on our website for future updates."],
    ["Hi, can I get a detailed report of my monthly transactions?", "Yes, you can generate a detailed monthly report of your transactions by logging into your account, going to 'Transaction History', and selecting 'Generate Report'.", "You can get a detailed monthly report by logging into your account, navigating to 'Transaction History', and clicking on 'Generate Report'."],
    ["I am traveling to the US. Can I use the app there?", "Yes, you can use the app in the US just like you do at home. Ensure you have an internet connection.", "The app will work in the US without any issues. Just make sure you have access to the internet."],
    ["How do I link my payment account to a new mobile number?", "To link a new mobile number, log in to your account, go to 'Account Settings', select 'Mobile Number', and follow the instructions to verify your new number.", "To add a new number, navigate to the 'Account Settings' section, select 'Mobile Number' and proceed with the steps to add and confirm the new number"],
    ["Can I receive notifications for transactions in real-time?", "Yes, you can enable real-time notifications for transactions by going to 'Account Settings', then 'Notifications', and turning on 'Transaction Alerts'.", "To see your transacation, log into your account and navigate to the 'Transaction History' section."],
    ["Hey, can I set up automatic transfers to my savings account?", "Yes, you can set up automatic transfers by going to 'Account Settings', selecting 'Automatic Transfers', and specifying the amount and frequency.", "You can arrange automatic transfers by going to 'Account Settings', choosing 'Automatic Transfers', and setting the desired amount and frequency."],
]

columns = ["question", "target_response", "new_response"]
typical_questions = pd.DataFrame(data, columns=columns)

test_suite = TestSuite(tests=[
        TestColumnValueMin(
            column_name=SemanticSimilarity(
            display_name="Response Similarity",
            with_column="target_response").
            on("new_response"),
            gte=0.9),
    ])

test_suite.run(reference_data=None,
            current_data=typical_questions)
print(test_suite.datasets().current)
df = pd.DataFrame(test_suite.datasets().current)        

            
  







