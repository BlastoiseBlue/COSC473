
Originally made by three students for the course COSC 473/573

For documentation on the API and how we access it, CovidActNow has provided the following: https://apidocs.covidactnow.org/access

Documentation of our architecture diagram can be found at the following: https://i.imgur.com/nR1ksp8.jpg

For future developers, use the template to recreate the project by:
•	Getting access to an API key (stored automatically as a secret)
•	Manually uploading a csv file to the resulting bucket (because we didn’t have a path for a definitive source)

GitHub repo for our project here: https://github.com/BlastoiseBlue/COSC473

Go to the following website URL to download the data: https://bigdata2bucket.s3.amazonaws.com/county-list.csv

Then they can open the file in Excel, Stata, or the application of their choice to view and filter the data.

The template describes all the resources required by the lambda function, including a bucket,
a secret to hold the API key, and a role that gives the lambda function access to them.

Any end user desiring to implement our code is recommended to fork this project,
so that they can implement whatever additional functionality they desire.

Thanks for taking a look at our project!
