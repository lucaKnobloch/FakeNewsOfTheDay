# User Guide

The project Fake News Of The Day (fakenod) is developed in connection with the Language Technology Group of the Universy of Hamburg. The Master project "Web Interfaces for Language Processing Systems" was the inializer for the tool.

In general is the idea to tackle two main issues with consuming news on a daily basis for people who are intrested in the daily news.

1. Time
    There are too many options to consum news. Either in a podcast as the spoek word or in a written word as newspapers.
    The idea to decrease the time to spent to get an overview of the daily happenings is on of the main aspects of the tool. The tool provides about articles the entites which are mentioned the most within an article. So that the reader gets an intuiton of the article and what are the main entites within. If the user is more intrested, the occurcane of the entity is provieded and the option to get leaded to the origin article.
    So that the user can be quickly get an overiews without reading the whole article.

2. Real / Fake News
    In the current time there are more and more fakenews provieded in the internet. There are already trackers published but they dont provide much information. The second idea is to give an overview of the daily news devided into fake and real news.
    A classifier is used to do a binary classification to add infromation to the user which articles might be fake and which might be real. The details of the provided entites in a article could trigger further investigation why this article might be classified as fake.

## The Pipeline

The main focus of the project was to create a pipeline to fullfill the following steps:

1. Crawling news on a daily basis
2. Classification of the articles
3. Extract the main information
4. Visualization to provide it to the end-user

For more information about the [Further information of the PipeLine](/PipeLine.md)
