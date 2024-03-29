# Terminology

todo: define ambiguous terms, then decide on naming

- estimator vs model
- How best to refer to specific parts of our data design?
  - dataset, data container
  - X & y, X-y-pair, labeled/unlabeled example, ...
  - distinguish between in-memory vs disk data?

Resources:

- <https://developers.google.com/machine-learning/crash-course/framing/ml-terminology>
- todo: find other autoritative sources

# Class diagrams

## Estimator

![Alt text](http://www.plantuml.com/plantuml/png/lLDTIyCm57tlhxZC1pzmWxqM7uPR5HzMP0CHH2Hcjnf8cv5xzo1p_zsqMudjCYk8UydMctFFERad6H4BowjSHwSmmKmLYfKf83CMvj9Oj7S5eys4n4ZL_zexi8u0rkALs0h96w1o--myXeMI_EIgbv1f8_WvsaIHr888nkMgCYL5ARVb0vKlDUPOC0KLxYrAHGuUR-bSQOPIQEs_RuOlLQUlZAqXIWgsPldXgpk7tiyCtomI_ThBT9u4sThOgy_187ZOCB9j8zfF9I5MkM0J3AQnwTsUB0IB62PkzLskJ9L8l9Tq8yrCiJjRexIqM4RxVO3pXsbzpERq3bYgMJqLG6qdD2-lz7XxRGpnaTJIz4X2YLjPoHHvTmdCN_LsF8T7-9z2JHf_mnltv23APzo5JDDkK6YsNT8_0dl37bpq-zLlw-t4y2u8H4TNzHJtUaPOB5Qv_W80 "Estimator")

## Data Abstraction

Creating a good abstraction for our data may be the most important part of this project, because this seems to be the biggest reason for the incompatibility *between* different frameworks, as well as the tight coupling of different components even *within* some of the major ML frameworks ([the worst of which I encountered with AWS Sagemaker](https://github.com/tloeber/email-classification#lessons-so-far)).

### Interfaces

Let's start by defining the *interfaces* we will implement. Actually, this is split into two different interfaces to account for the two different kind of operations we want to perform: *transforming between different formats*, and *splitting* the overall data. We will think of the former as simply the actual **DataSet** with which we will we working with, and the latter as a **container** for DataSets, because it contain the seperate subsets for training, validation, and testing. Let's first start by looking at this design using a basic visualization:
![Alt text](../img/data_design.jpg)

We can translate this into object-oriented design as follows:
![Alt text](https://www.plantuml.com/plantuml/png/jPLHRzf03CVVxrDOl9IqWW-04AgsgjhU9lMneCZa7BWgkOjyPXlR-jrt5m8iD8s2fhvnlf__zjz9pBqNPDcLXLB62d6E6S5eFlzwF2mMI_k0Wf-T5JIM-7GpWladz1GldqZE2V1R0TnjI5BXa97g08oJ6NJ19vAy30A_Os42PzmmNIoAVkvLALnxOSm4iWAzXvRPTos6nC5J-ZETNgZEm9HLGILPyQflybtLH-S1Ut6C6qfpnoNAE0dncxkAs1iVJz7Tq2udR3PRcIo6jJ23KTkHyR2XyCDaO2mq_DAEBP7s80xM11KobYG1-aKQrdj0kCsSpJZ4Reyv8FkAab7VK9w4TvdicFIRlkh9pET14YMmERiohT1gz6CTs1bKUXgJ7cCdIGTiTsMrJv4Pzqs6hQPMru6Q5tSKJDfgXykMGF9ljdhjzKIbkTBNYtUswT4B9-yGXR7a-p5jCcc8-BCBAOoNrEKrwYzPSOTUahh2ATBKReVhMiaXkGcrjSDT33p7qwf_Pe-cwFuuEXmoPU9uFwvGjZDuE9w_XMENtpn8-nhsJJ-nMAHNHyjdpUH2y00q6ibbVlGqx3EFY-EQbx-zLlwd1fNcu-iq3x1VNRNNJ7jB3H-BVxDybjQjNoYJSp5ZDylJweBJQwUKklbYj2OBoEn-rDiiDp-Xe5mcuWujWMDDhAvfQ_AyhMLNZQTh7uDIwfwiZl_TVm40 "data_design")

#### Data*Set* Interface

Let's first look at the interface for the Data*Set*s: This interface is to provide a contract for the kind of objects that our data container returns (whether we retrieve the complete dataset or a proper subsets). *Its main purpose is to decouple our data abstraction from the specific way this data is represented (whether in persistent storage or in-memory)*. To this end, it contains two important sets of methods:

- a *constructor* for each permissible format;
- a to_${FORMAT}() method for each permissible format, which allows us to *access* the data in the desired *format*.

Since be permissible formats are specific to the concrete data set type, the methods are not part of the general BaseDataSetInterface.

~~This raises the question how we can constrain the permissible data formats to only those that make sense for a given *kind* of data? For example, while it would be natural to create a structure data set from a pd.DataFrame, this input format would not make sense when working with image data. To this end, we use an Enum to model the possible datatypes that a given type of data could represent: For example, a structured dataset would be commonly stored on disk in parquet, csv, or JSON Lines format, or in-memory as a Pandas DataFrame. (Note that the *type in Python* corresponding to a given return format is not necessarily the same: For example, when we get our dataset in csv format, the return type would be `str`, or even `None` if we write to a file. We will deal with these details later).~~

![Alt text](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuU9AJ2ekAKfCBb58paaiBbPmIYnETKaiINJBByfDB57WuahDAyrL22ufAaqkAIrAJK6Iix5Hq73LIIzAJStJL705AREpKwZcKb08S0mA37KD0RASWyE0f5UmlvyFIDmbtiKnnD4joD7NbQiMPdHgRYO9niECW-jtoyn99UoW40ye5U_Z6Hm2qepcKPiQNLsitiIk4E5emeeHBkJYSaZDIm45Em00 "data_format")

#### Data*Container* Interface

Below is the corresponding UML diagram. It shows the idea of data containers by leveraging *parameterized classes* (a.k.a. *templates*), which we can implement in Python using [Generics](https://mypy.readthedocs.io/en/stable/generics.html): The Data**Container**Interface provides a *contract for how we can retrieve the relevant subsets* (training, test, and validation set, as well as the whole dataset) *from our data abstraction*. However, it *does not know anything about these subsets* except how to retrieve each – from the data container's point of view, these could be any kinds of objects. It is thus similar to a collection (such as list, set, or dictionary) in Python. When using this inbuilt collections, we often want to restrict the type of elements we can put into our collection to only those that make sense in our domain. We would do this by using `list[string]` or `list[int]`, etc. We will use this same principle for modeling our data containers, with two further modifications: Firstly, since there is no inbuilt type for the datasets we want to put into our container, so we need to define our own custom class for data sets. Secondly, we want to be able to use *sub*types of dataset (such as *structured* dataset or *image* dataset) whenever we instantiate a concrete data containers. The challenge is that for a *given* data container, all its elements need to be of the *same* subtype: For example, if we are working with structured data, the training, test, and validation sets in our data container should all be of type StructuredDataSet, whereas if we work with image data, all subsets should be of type ImageDataSet.

In the absence of Generics, we could model this by making the DataContainerInterface an *abstract* interface that we do not implement directly, and instead create subclasses for data container interfaces for each specific dataset type (StructuredDataContainerInterface, SemiStructuredDataContainerInterface, ImageDataContainerInterface, etc.). I actually started out with this approach, but while this may seem on the surface like a simpler solution than to use Generics, it soon leads to greater complexity because it multiplies the number of necessary classes. This is especially true for a general framework such as ours, where we want to follow the famous design principle to depend on abstractions rather than concretions: Since we have to duplicate this structure for both interfaces and implementation, we end up with a BaseDataContainerInterface, StructuredDataContainerInterface, ImageDataContainerInterface,... as well as BaseDataContainer, StructuredDataContainer, ImageDataContainer, etc. Note that either way we will end up with this proliferation of classes for Data*Sets* - but by contrast to Data*Container*(Interface)s, it actually serves the important purpose of defining the specifics for that kind of data: The interfaces specify a specific contract from which formats a given kind of dataset can be created, to which formats it can be converted, etc.; and the implementations come up with a concrete way of achieving this behavior. However, there is no need to duplicate this logic at the level of the data container.

This is where Generics come in: They allow us to define the DataContainer simply as a container of objects that satisfy the BaseDataSetInterface. At the same time, however, Generics allow us to make sure that [all the objects in the container are of the *same* subtype](https://stackoverflow.com/questions/58903906/whats-the-difference-between-a-constrained-typevar-and-a-union).

![Alt text](http:////www.plantuml.com/plantuml/png/ZPBBQiD034NtynKYAvkIV40m9hIbq7Mt1IFRiZim3oCfBUdZtpjEI49B4cPbP9qhSm_UY2BhrZjZR53Y0Jk2HLKz7uUwVWsFgFWGWw8DnAVD0gfx59gNBwJd07mPWBkHj55EYQPFG56kuH9y8aaq2tn7PnDdOzvTTEuszsDCvr04_dIysYpnsNA-Lwj_LzTW_UJ8Kr0njuHV-lhYuBMgEYRKX0qSVJD4zgZ5uN7k-BIVopcWCGEQNOb6nf6EzFxz1rkbgy5a8rl7aktufiiwhsio9J1I8BOTs0158Ee5D49BC26Z9qsxJ-gXtG62R5lTJGHnA8tPKEZdF_eN "data_container_interfaces")

(Note that this interface does not contain a method to split the data, because this task can be handled by our data abstraction under the hood *if* necessary - and it will in fact not always be necessary, because we should allow our data container to be constructed from data that already comes pre-split.)

Also note that we will leave it up to the implementation whether the data container "has a" (is a composition or aggregation of) training set, validation set, and test set; or whether it simply "has a" single/combined dataset and fetches  the relevant subsets when requested. Our data container interface simply provides a contract for how we should be able to *retrieve the subsets* (as well as the complete dataset).

### Implementation

Here is my proposal for how to implement the above interfaces: Our *container* class "has a" data splitter object (which contains concrete logic for how to split the data into training, validation, and test set, and uses information about the dependency relationship between the individual records to carry this out properly), as well as how to retrieve each of these subsets. By using an aggregation relationship, the splitter class is easily reusable. In particular, a given splitter can be used for different datasets: For example, the logic for performing a time-series split is the same for a structured dataset and an image dataset.

Note that we even require this splitter to be present in the case where the data already comes pre-split. Here, it still performs the important job of  retrieving the relevant subsets (including the whole dataset). Note also that this PreSplitDataSplitter will indeed implement the _split_data() method to satisfy the common interface, but since it should never be called, this method will always raise a (semantic) error.

![Alt text](http://www.plantuml.com/plantuml/png/dLLHQzim47wkVeKU7TQ4iKVJbMxT2Xsi6_LW3sEOgtr91RPaJkUDqkw_pvQQo3YNPkmbHBhlEttttHs-y0p4VTiezHuyVW26IsSPZ4NIRhdKszkYQmmpaixrFNWDEgknmGqmUirk8R1NP3Rtl7ewJpcG1thl1qfMEUkP-egnrcjohGPRQqBkoVg5Kd0tHA5YNJNWlTxF_gYqVgNNZbhWV1U_2kSGEZkh287n_7nCN_h-pYFxZ6dWbnuvdygwjeoqXWfFzIzeJ0rit8ieHi-7umj9GUNQha76aPQbmyivs9MnnamkTQ7-o6QbbaMlbb5oHwvpD5QNwtNZWFLR_Nhr9W1IvI_2IZ_cBGSaP57a1hcCliulqUy1qoin4Yg8mgzjZHqEFvQd-f-ZtqoB1P91BnKt14ipCitQ8FaXQMHTDhrd9Am5KXLZ8g_eW0qq4iivgeq5bX_yIXW8KsOa1ekCtOmzdnc-kzhErRxJkIwm1Skc-aZaAFXPkVREM9mOkTVxiwVbyg2nCbesMWRB_ifOoLCPAPge3WywydDl2A56Iajo6yuXz9iCJqFVntEmSRQdH_Pj8B3x1z0uwvuTmGQtw70_Iep_Wg9Ctk2f_51RfEL3ApzZw-ZX5Zj2ZvR3_AJf0rk3t_5EHbgkkteLr16qk8D-AhxSp86rgVZ7E_jmgeUVdxAov5vKzbn6hc-SnP4oLRB3dOYmg686If19WzF7AFaYVue4Lj9ycALcoUCSJkmK0Sb4fMRlXFZK1H6GwjywKeJFOhzTAUJ7uqEQEDAe7eUcVXJOclzG8F1a5H9SLd9bchJTHmK4kFYa09ZDLkp4NjK2H317W4sKAtM1jkxRHlq5 "data_container_implementation")

# Pipeline

Finally, here is a complete ML pipeline:
![Alt text](http://www.plantuml.com/plantuml/png/XP91ImCn48Nl-ok6dbIeuBMd8kfDASLx6RFZDZIRX9afMCJ_RhAfeTlAzXJoyhsypPjTYYBhldUDSIW2Anl9MK_mtG3mtj_SBk0jU6f-cZ-2QSN1a4ZWWOfCiGWPVaB55yR-nF4iQdlK8_vfDNEleILNtAqrW-JZFJBZ8QbY0jDmNJexoGwYP-59kPB-5ObjJrxV6SsEYi-5hZuDe2FT94Kk4ijdhgcpedmefGmRuZDxdy7wi56yG-kFiLHscLjJ3An9Criokys7nI7-CQtbADzHnp5xcC7TV9xNyGGMi4K1_9-ipKzZuredqSis9_5nVPDeBQfYI_9j_ZD_0G00 "Pipeline")
Note that this is part of the design is least mature and lowest priority, because there already exist a number of good pipeline tools such as MLFlow Piperlines. Thus, I still need to decide to what extent the pipeline abstraction is even needed. However, a good *data* abstraction - which I am first focusing on developing – will be key in order to have minimal coupling between pipeline components. For example, this is not only necessary to decouple the preprocessor from the estimator, but also so we can easily re-use model quality evaluation (accuracy, etc.) and explainability tools.
