let currentChosenModel

(async () => {
    currentChosenModel = await getCurrentModel();
    let tag = document.querySelector("#chosenModelWrapperTag");
    tag.textContent = currentChosenModel.filename;
})()

async function getCurrentModel(){

    const result = await AJAXCall({
        phpFilePath: "/include/getCurrentModel.php",
        rejectMessage: "fetching current model failed",
        type: "fetch",
        params: ""
    });

    console.log("chosen model: ", result);

    return result[0];
}

let originalChosenModel = { ... currentChosenModel };

const predictionModelsBody = document.querySelector(".prediction-models-body");

(async () => {

        // get data here

        let models = await AJAXCall({
            phpFilePath: "../include/getAllModels.php",
            rejectMessage: "Getting Models Failed",
            params: "",
            type: "fetch"
        })

        console.log("models: ", models);

        let groupedModelData = groupModelsBy(models, "type");

        console.log(groupedModelData);

        // let models = [{
        //     modelType: "VGG16",
        //     models: [
        //         { name: "VGG16-VARA01", id: "a", accuracy: 99.4}, 
        //         { name: "VGG16-VARA01", id: "b", accuracy: 76.7}
        //     ]
        // }, {
        //     modelType: "ResNet50",
        //     models: [
        //         { name: "RSNT50-VARA03", id: "c", accuracy: 99.4}, 
        //         { name: "RSNT50-VARA04", id: "d", accuracy: 76.7}
        //     ]
        // }, {
        //     modelType: "CNN",
        //     models: [
        //         { name: "CNN-VARA03", id: "e", accuracy: 99.4}, 
        //         { name: "CNN-VARA04", id: "f", accuracy: 76.7}
        //     ]
        // }]

        groupedModelData.forEach( modelType => {

            let modelChoiceContainer = document.createElement("div");
            modelChoiceContainer.className = "model-choice-container";
        
            let modelTypeTitle = document.createElement("h4");
            modelTypeTitle.textContent = modelType.modelType;
        
            let innerModelContainerList = document.createElement("div");
            innerModelContainerList.className = "inner-model-container-list";
        
            modelType.models.forEach( model => {
                const modelRow = createModelRow(model);
                innerModelContainerList.append(modelRow);
            })
        
            modelChoiceContainer.append(modelTypeTitle)
            modelChoiceContainer.append(innerModelContainerList)
        
            predictionModelsBody.append(modelChoiceContainer);
    
        })
    }
    
)();

function groupModelsBy(data, key){

    let result = [];

    let tempObject = {};

    data.forEach( element => {
        console.log(element[key])
        tempObject[element[key]] == null ? tempObject[element[key]] = [] : false;
        tempObject[element[key]] = [ ...tempObject[element[key]], element ];
    })

    console.log(tempObject)

    let entries = Object.entries(tempObject);

    entries.forEach( ([key, value] = entry) => {
        result.push({
            modelType: key,
            models: value
        })
    })

    return result;

}

function confirmModelChanges(){

    originalChosenModel = { ...currentChosenModel };

    let tag = document.querySelector("#chosenModelWrapperTag");
    tag.textContent = currentChosenModel.filename;

    console.log(`Confirmed, ${currentChosenModel.filename}`);
    // set globalCache.
    // upload to database;
    checkConfirmButton()     
    closePopup(".model-choice-overlay");  

}


function createModelRow(rowData){

    let modelRow = document.createElement("div");
    modelRow.className = "model-row";
    modelRow.setAttribute("data-id", rowData.id);

    let modelRowName = document.createElement("div");
    modelRowName.className = "model-row-name";
    modelRowName.textContent = rowData.filename;

    let modelRowAccuracy = document.createElement("div");
    modelRowAccuracy.className = "model-row-accuracy";
    modelRowAccuracy.textContent = rowData.accuracy + "%";

    let modelTicked = document.createElement("div");
    modelTicked.className = "model-ticked";

    let modelTickedImage = document.createElement("img");
    modelTickedImage.src = "assets/icons/check.png";

    modelTicked.appendChild(modelTickedImage);
    modelRow.appendChild(modelRowName);
    modelRow.appendChild(modelRowAccuracy);
    
    if (rowData.id == currentChosenModel.id ) {
        console.log("yes");
        modelRow.className = "model-row selected"
        modelRow.appendChild(modelTicked);
    }

    modelRow.addEventListener("click", () => {
        uncheckAllModels();
        modelRow.className = "model-row selected";
        modelRow.appendChild(modelTicked);
        currentChosenModel = { ...rowData };
        console.log("current model id: ", currentChosenModel.id);
        console.log("original model id: ", originalChosenModel.id);
        checkConfirmButton();

    })

    return modelRow;

}

function checkConfirmButton(){

    const button = document.querySelector(".confirm-model-changes-button");

    if(currentChosenModel.id == originalChosenModel.id){
        button.setAttribute("disabled", "true");
        button.textContent = "No Changes Made";
    }
    else { 
        button.removeAttribute("disabled");
        button.textContent = "Confirm Changes";
    }

}

function uncheckAllModels(){
    let modelRows = predictionModelsBody.querySelectorAll(".model-row");
    modelRows.forEach ( row => { 
        row.className = "model-row";
        let modelTicked = row.querySelector(".model-ticked"); 
        if(modelTicked) modelTicked.remove();
    });
}

