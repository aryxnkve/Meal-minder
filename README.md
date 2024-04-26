# NutriBuddy

The project aims to develop a personalized meal planner application that utilizes data from various sources, including nutritional databases, user input, and meal suggestion algorithms. The application will be developed using modern web and mobile technologies, leveraging frameworks such as React.js for frontend development and Node.js for backend functionality. The expected deliverables include a user-friendly interface for meal planning, calorie tracking features, personalized meal suggestions, and data visualization capabilities.

## Documentation

[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1r6Cg_miHqOiVv43CM6GhOtq1ZWK9lf6mIlYW7VNuSVk)

## Data Sources

### Food Image Classification Dataset

The dataset contains 24K unique images obtained from various Google resources
Focuses on 35 varieties of both Indian and Western appetizers
Meticulously curated images ensuring diversity and representativeness
Provides a solid foundation for developing robust and precise image classification algorithms
Encourages exploration in the fascinating field of food image classification

### Foodies AI

This dataset contains a collection of images showcasing various dishes from Indian cuisine. The images cover a wide range of traditional and popular dishes such as naan, dosa, biryani, samosa, and more. Each image is labeled with the name of the dish it represents. The dataset is suitable for tasks such as image classification, object recognition, and culinary research. It can be used by researchers, data enthusiasts, and machine learning practitioners interested in exploring and analyzing Indian culinary heritage.

### CNFood

Contains a dataset of 241 Chinese dishes with 191,811 images. There are 170843 images in the training set and 20943 images in the validation set. All images are resized to 600x600. As some of the images in the dataset are from ChineseFoodNet, they are not supported for commercial use.

### ChineseFoodNet

ChineseFoodNet aims to automatically recognizing pictured Chinese dishes. Most of the existing food image datasets collected food images either from recipe pictures or selfie. In the dataset, images of each food category of the dataset consists of not only web recipe and menu pictures but photos taken from real dishes, recipe and menu as well. ChineseFoodNet contains over 180,000 food photos of 208 categories, with each category covering a large variations in presentations of same Chinese food.

### Calorie Predictor Dataset

A novel food image data set with volume and mass records of foods, and a deep learning method for food detection, to make a complete calorie estimation. The data set includes 2978 images, and every image contains corresponding each food's annotation, volume and mass records, as well as a certain calibration reference. To estimate calorie of food in the proposed data set, a deep learning method using Faster R-CNN first is put forward to detect the food. And the experiment results show our method is effective to estimate calories and our data set contains adequate information for calorie estimation. Our data set is the first released food image data set which can be used to evaluate computer vision-based calorie estimation methods.

## Tools and Technologies:

- FrontEnd : StreamLit
- Backend : FastAPI
- Database : PostGreSQL
- Cloud : GCP
- Model Training : PyTorch
- Automation : Airflow

## Pipelines

#### Capture Calories:

![Architecture Diagram ](images/1.png)

#### RAG to suggest Meals as per Calories

![Architecture Diagram ](images/2.png)

#### Model Training: Custom Model training for Cuisine classification and Calorie estimation

![Architecture Diagram ](images/3.png)

#### Data Scraping

![Architecture Diagram ](images/4.png)

## References

- [Food Image Classsification Dataset](https://www.kaggle.com/datasets/gauravduttakiit/food-image-classification)
- [Foodies AI](https://www.kaggle.com/datasets/jvageesh11/foodies-ai-food-image-classification-challenge)
- [CNFood](https://paperswithcode.com/dataset/cnfood-241)
- [ChineseFoodNet](ChineseFoodNet)
- [Calorie Predictor Dataset](https://github.com/Yiming-Miao/Calorie-Predictor/tree/master/Dataset)
