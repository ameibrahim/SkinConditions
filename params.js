let data = {
    id: "4353535",
    imageName: "fkdfdf.jpg",
    param3: 3,
    param4: "499343040340340403040400340340o92424244",
    data: "03/06/07"
}

function createParamatersFrom(data){

    let params = "";
    let entries = Object.entries(data);

    entries.forEach( ([key, value], index) => {
        let parameter = `${key}=${value}`
        index < (entries.length - 1) ? 
        params += parameter + "&&": 
        params += parameter;
    })

    return params

}

let params = createParamatersFrom(data);
console.log(params)