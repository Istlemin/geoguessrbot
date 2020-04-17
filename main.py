
from dataset_loader import DatasetLoader
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
  
from CNN_model import CNNModel
from no_input_model import NoInputModel

from utils import geoguessr_score

def average_score(model, images_to_predict,labels_to_predict):
    predictions = model.predict(images_to_predict)
    score_sum = 0
    num_rounds = 0 
    for guess,answer in zip(predictions,labels_to_predict):
        score_sum += geoguessr_score(guess,answer)
        num_rounds += 1
    return 5*score_sum/num_rounds

def plot_loss_histories(training_loss_histories,validation_loss_histories):
    plt.figure(figsize=(10,10))
    for model_name, loss_history in training_loss_histories.items():
        if model_name != "noinput":
            plt.plot(loss_history, label = model_name+' training loss')
    for model_name, loss_history in validation_loss_histories.items():
        if model_name != "noinput":
            plt.plot(loss_history, label = model_name+' validation loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='lower right')
    plt.show()

def predict_images(models, images_to_predict,labels_to_predict):

    for model_name,model in models.items():
        print("Average Score "+model_name+": ", average_score(model,images_to_predict,labels_to_predict))

        predictions = model.predict(images_to_predict)
        plt.figure(figsize=(10,10))
        plt.title(model_name)
        print("yes")
        for i in range(9):
            plt.subplot(3,3,i+1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            print(images_to_predict[i].shape)
            plt.imshow(images_to_predict[i])
            plt.xlabel(str(geoguessr_score(predictions[i],labels_to_predict[i]))+"\n"+str(list(predictions[i])))

        plt.show()


def main():
    dataset_loader = DatasetLoader("../geoguessrBotDatasets/geoguessrWorld/",(48,64),"coordinates")
    train_dataset = dataset_loader.load_dataset(0,9000,"train_dataset")
    val_dataset = dataset_loader.load_dataset(9000,10000,"validation_dataset")

    models = {
        "CNN": CNNModel(),
        "noinput": NoInputModel(),
    }

    validation_loss_histories = dict()
    training_loss_histories = dict()

    for model_name,model in models.items():
        model.train(train_dataset,val_dataset,100)
        training_loss_histories[model_name] = model.training_loss_history
        validation_loss_histories[model_name] = model.validation_loss_history

    images_to_predict, labels_to_predict = next(iter(val_dataset))
    predict_images(models,images_to_predict,labels_to_predict)

main()
