### **Top 3 similar Email based on Text similarity technique**

---

>**Email ID** - User's regular email id, used for normal correspondence

>**FB Email ID** - User's Email id, used to register with Facebook. 

---

>Now our **objective** is to find out the top 3 most similar email ids from the classroom *user* table *mdl_user* for each user in our *user_details* table.

few points -

- In case email from any of the "Email ID" or "FB Email ID" field is present in the "mdl_users" table, that email is the Facebook email of the user so text-matching is not applied.
- Final output is of the following format:
> First-name_from_users_details | last-name_from_user_details | Email ID_from_user_details | FB_Email_ID_from_user_details | Matched_Email_1 | Matched_Email_1_Score | Matched_Email_2 | Matched_Email_2_Score | Matched_Email_3 | Matched_Email_3_Score | Best Matched_Email
