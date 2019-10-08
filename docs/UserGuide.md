# User Guide

The project Fake News Of The Day (fakenod) is developed in connection with the Language Technology Group of the University of Hamburg. The Master project "Web Interfaces for Language Processing Systems" was the initiator for the tool.

In general, the tool  tackles two main issues with consuming news daily for people who are interested in the daily news.

1. ## Time

    There are too many options to consume news. Either in a podcast as the spoken word or in a written word as newspapers.
    The idea to decrease the time to spent to get an overview of the daily happenings is one of the main aspects of the tool. The tool provides about articles the entities which are mentioned the most within an article. So that the reader gets an intuition of the article and what are the main entities within. If the user is more interested, the occurrence of the entity is provided and the option to get led to the origin article.
    So that the user can quickly get an overview without reading the whole article.

2. ## Real / Fake News

    In the current time, there are more and more fake news provided on the internet. There are already trackers published but they don't provide much information. The second idea is to give an overview of the daily news divided into fake and real news.
    A classifier is used to do a binary classification to add information to the user which articles might be fake and which might be real. The details of the provided entities in an article could trigger further investigation of why this article might be classified as fake.

## The Pipeline

The main focus of the project was to create a pipeline to fulfill the following steps:

1. Crawling news daily
2. Classification of the articles
3. Extract the main information
4. Visualization to provide it to the end-user

For more information about the [Pipeline](./PipeLine.md)

For more information about the [Usage of the front-end](./Front-end-user-guide.md)

For more information about the [Technologie Guide](./TechnologieGuide.md)
