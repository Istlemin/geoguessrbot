
from dataset_loader import DatasetLoader
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
  
from CNN_model import CNNModel
from no_input_model import NoInputModel

def main():
    dataset_loader = DatasetLoader("data/locationsGeoguessr/",(48,64),"coordinates")
    train_dataset = dataset_loader.load_dataset(0,9000,"train_dataset")
    val_dataset = dataset_loader.load_dataset(9000,10000,"validation_dataset")

    models = {
        "CNN": CNNModel(),
        "noinput": NoInputModel(),
    }

    loss_histories = dict()

    for model_name,model in models.items():
        model.train(train_dataset,val_dataset,100)
        loss_histories[model_name] = model.loss_history

    plt.figure(figsize=(10,10))
    for model_name, loss_history in loss_histories.items():
        plt.plot(loss_history, label = model_name+' loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='lower right')
    plt.show()

    images_to_predict, labels_to_predict = next(iter(val_dataset))

    test_predictions = models["CNN"].predict(images_to_predict)
    plt.figure(figsize=(10,10))
    print("yes")
    for i in range(9):
        plt.subplot(3,3,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        print(images_to_predict[i].shape)
        plt.imshow(images_to_predict[i])
        plt.xlabel(str(list(labels_to_predict[i].numpy()))+"\n"+str(list(test_predictions[i])))

    plt.show()

main()