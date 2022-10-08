# CRM Prototype Application (Flask)

This web application has been created as part of MSc Datascience thesis in Flask. Backend of the applicaiton is PostgreSQL. 

The application consists of 2 pages - 
1. The Dashboard page which shows the list of leads generated from the propensity model. The leads are sorted on descending order based on the propensity score. Each Lead has a show detail button which provides more information about the lead and an option for front line to provide feedback on the lead.
2. The About Application page which details about the Thesis topic and artifacts.

<u>Dashboard page</u>

![image](https://user-images.githubusercontent.com/95563854/194727608-be841c9d-8322-495b-b074-8b7e61689b3a.png)

<u>Details popup</u>

The top influencers for the lead (3 positive and 3 negative), SHAP force plot along with a Tableau web embedding displaying balance trend of the customer is included in the popup.

![image](https://user-images.githubusercontent.com/95563854/194727656-845e3339-254a-4402-9d59-2ecf316ac598.png)


<u>About Application page</u>

![image](https://user-images.githubusercontent.com/95563854/194727675-82e1aea6-4129-4845-bcc1-a9419aae4e0a.png)
