### **Top 3 similar Email based on Text similarity technique**
We have a lot of users in our "user_details" table and there are two email fields associated with each of them

---

>**Email ID** - User's regular email id which they use for normal correspondence

>**FB Email ID** - User's Email id they have used to register with Facebook. 

---

*In case, Email ID is the email they have used to register on Facebook as well then this field is not required.*

However, all that being said, we don't have the correct Facebook emails for a lot of users. There are a few reasons for that one of which is that the additional field of FB Email ID was added later on in the process.

>Now our **objective** is to find out the top 3 most similar email ids from the classroom *user* table *mdl_user* for each user in our *user_details* table.

However, there are few points you should keep in mind while implementing this -

- In case email from any of the "Email ID" or "FB Email ID" field is present in the "mdl_users" table, directly use that email as this means that we already have the Facebook email of the user.
- Final output should be of the following format:
> First-name_from_users_details | last-name_from_user_details | Email ID_from_user_details | FB_Email_ID_from_user_details | Matched_Email_1 | Matched_Email_1_Score | Matched_Email_2 | Matched_Email_2_Score | Matched_Email_3 | Matched_Email_3_Score | Best Matched_Email