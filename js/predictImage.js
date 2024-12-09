function handlePredictingImageChange(event) {
  let file = event.target.files[0];

  let previewIMG = document.querySelector(".image-predict-chosen-preview");

  previewIMG.zIndex = 2;

  loadImage(file, ".image-predict-chosen-preview");
  globalCache.put("hasImageBeenSelected", true);
  globalCache.put("selectedImageForPrediction", file);
}

function resetPredictionOverlay() {
  document.querySelector(".image-predict-chosen-preview").src = "";
  globalCache.put("hasImageBeenSelected", false);
  globalCache.put("selectedImageForPrediction", null);
}

async function startPrediction() {
  openPopup(".loader-view.predict-loader");

  const selectedImage = globalCache.get("selectedImageForPrediction");
  const hasImageBeenSelected = globalCache.get("hasImageBeenSelected");
  const {
    id: modelID,
    filename: modelFilename,
    featureInputSize: modelInputFeatureSize,
  } = currentChosenModel;

  if (!hasImageBeenSelected) {
    //TODO:  showSelectImageToast();
    console.log("Image has not been selected");
    return;
  }

  try {
    //TODO: Uploading Images Doesn't Work ??? On Chrome Dev
    let fileUploadResult = await uploadFile(selectedImage);
    let { newFileName: imageName, fileSize } = fileUploadResult;

    let domain = getDomain();
    console.log(domain);

    let data = {
      imageName,
      modelFilename,
      modelInputFeatureSize,
      domain,
    };

    //TODO: detectPredictImage

    // var jsonString = JSON.stringify(data);
    let tickPredictionResult = await getResultsForTick(
      createParamatersFrom(data)
    );

    console.log(tickPredictionResult);

    let parameters = {
      id: uniqueID(1),
      userID: "3333434",
      date: getCurrentTimeInJSONFormat(),
      modelID,
      result: tickPredictionResult.predicted_class,
      imageName,
      fileSize,
    };

    const options = filterOptionsOff(parameters.result);

    let params = createParamatersFrom(parameters);

    console.log("params to save to database: ", params);

    await uploadPredictionToDatabase(params);
    closePopup(".loader-view.predict-loader");
    closePopup(".overlay.prediction-overlay");

    let changePredicitionButton = document.querySelector(
      ".change-prediction-button"
    );

    changePredicitionButton = clearEventListenersFor(changePredicitionButton);
    changePredicitionButton.addEventListener("click", () =>
      handleChangePrediction({ ...parameters, options })
    );

    // await renderPastPredictions();
    await handlePredictionReview({
      ...parameters,
      ...currentChosenModel,
      ...tickPredictionResult,
    });
  } catch (error) {
    console.log(error);
  }
}

async function confirmPredictionChanges(e) {
  e.preventDefault();
  const loader = document.querySelector(".change-prediction-loader");
  loader.style.display = "grid";

  const predictionChanges = globalCache.get("predictionChanges");
  if (predictionChanges.comment && predictionChanges.comment.length < 1)
    predictionChanges.comment = "None";

  let params = createParamatersFrom(predictionChanges);

  if (predictionChanges) {
    try {
      await AJAXCall({
        phpFilePath: "../include/changePrediction.php",
        rejectMessage: "Changing Prediction Failed",
        params,
        type: "post",
      });

      // move file
      await AJAXCall({
        phpFilePath: "../include/copyFile.php",
        rejectMessage: "Copy File Failed",
        params: createParamatersFrom({
          imageName: predictionChanges.imageName,
          uploadFolderPath: "../uploads/",
          newFolderName: predictionChanges.result,
        }),
        type: "post",
      });
    } catch (error) {
      console.log("move file error: ", error);
    } finally {
      setTimeout(() => {
        loader.style.display = "grid";
        closePopup(".change-prediction-overlay");
        changePredictionValue(predictionChanges.result);
      }, 1000);
    }
  }
}

function isProjectRunningLocally() {
  let currentURL = new URL(window.location.href);
  return currentURL.hostname == "localhost" ? true : false;
}

function getResultsForTick(params) {
  return new Promise(async (resolve, reject) => {
    let hostname = isProjectRunningLocally()
      ? "127.0.0.1:8001"
      : "skin.api.aiiot.live";
    console.log("hostname: ", hostname);
    let url = `https://${hostname}/predict/?${params}`;

    // http://127.0.0.1:5000/predict/?imageName=test6.jpeg&&modelInputFeatureSize=128&&modelFilename=cnnmodel.keras&&domain=localhost:8888

    // http://165.22.182.47:8033/predict/?imageName=1717389419.jpg&&modelFilename=VGG16-VARA01b-32x32-EP15-ACCU99-02-06-2024.keras&&modelInputFeatureSize=32

    let result = await fetch(url, {
      method: "GET",
    });

    let JSONResult = await result.json();
    let classification = JSONResult.classification;
    resolve(classification);
  });
}

async function uploadPredictionToDatabase(params) {
  try {
    let result = await AJAXCall({
      phpFilePath: "../include/savePrediction.php",
      rejectMessage: "Saving Prediction Failed",
      params,
      type: "post",
    });

    console.log(result);
  } catch (error) {
    console.log(error);
  }
}

function changePredictionValue(value) {
  const predictedClass = document.querySelector("#predicted-class-placeholder");
  predictedClass.textContent = value;

  const stagesContainer = document.querySelector(".stages-container");
  stagesContainer.style.display = "none";
}
