
//Delete param form
function deleteParamForm(){
	if(document.getElementById("form"))
		document.getElementById("form").remove();
}

//function to call when another method selected
function callOnMethodChange(){
	let endpoint = document.getElementById("acts").value;
	if(endpoint=="split")
		requestToRespondingAction([]);
	else{
		deleteParamForm();
	}
}

//resolve changes
function wait() {
  return new Promise(resolve => {
    resolve();
  });
}

//write results to prediction element
async function writeToPredictionElement(responseArray){
	if(Array.isArray(responseArray))
		responseArray = responseArray[0]
	predLoc().innerText=responseArray.toUpperCase();
	await wait();
}


var currentArgs;
function destroyAndReturn(){

	request = {"args": currentArgs,"params":null}
	let inputs = document.getElementById("form").getElementsByTagName("input");
	let obj = {}
	for(let i=0;i<inputs.length;i++)
		if(inputs[i].value!="null"){
			let parsed = parseFloat(inputs[i].value); 
			obj[inputs[i].name] = isNaN(parsed) ? inputs[i].value  : parsed;
		}

	request["params"] = obj;
	writeToPredictionElement("Training...")
	POST("/train",request,writeToPredictionElement)
	deleteParamForm();
}

//Ask for parameters before training
function askForParams(paramSet){

	//get params of selected model
	let currentParams = paramSet[0]

	//Input Form Builder
	function createInput(name,value){
		return '<label for="'+name+'">'+name+'</label><br> \
    	<input type="text" id="'+name+'" name="'+name+'" value = "'+value+'"><br> '
	}

	//Build form
	let start = '<div id="form" >';
	let end = '<button onclick="destroyAndReturn();">send</button> </div>';
	for(let key in currentParams) 
  			start+=createInput(key,currentParams[key]);
	
	start+=end;

	//Append form to element
	document.getElementById("prediction").innerText = "";
	document.getElementById("description").innerText = "";
	document.getElementById("prediction").innerHTML +=start;
	document.getElementById("form").focus();
}


function requestToRespondingAction(args){


	let endpoint = document.getElementById("acts").value;

	let request = {
		"text": getTextInput(),
		"args": args,
	}

	if(endpoint=="train" && args[0]!="ALL IN ONE"){
		currentArgs = args
		if(document.getElementById("acts").value!="train")
			writeToPredictionElement("Enter parameters")
		POST("/"+"param",request,askForParams)
		return;
	}
	if(endpoint=="split"){
		test_ratio = getInput("Enter test ratio");

		//If input window closes, return
		if(test_ratio==null || test_ratio === "undefined")
			return
		request = {"test_ratio": test_ratio}
	}

	writeToPredictionElement(endpoint+"ing...")
	endpoint = endpoint.toLowerCase()
	POST("/"+endpoint,request,writeToPredictionElement)

}

function getArgFromElement(element){
	return element.innerText.split("\n")[0];
}
function getParent(element){
	return element.parentNode;
}

function copyObject(objectToCopy){
	return JSON.parse(JSON.stringify(objectToCopy));
}
function click(event){

	currentElement = event.target; 
	current =  getArgFromElement(currentElement);
	args = [current];

	//Reverse pathfinding to extract model argument tree
	while(current!="ALL IN ONE" && currentElement!=null){
		if(currentElement.tagName=="MENUITEM" && !args.includes(current))
			args.push(current);
		currentElement = getParent(currentElement);
		current = getArgFromElement(currentElement);
	}

	let desc = ""
	let node = copyObject(model_tree)
	for(var i = args.length-1;i>=0;i--){
			node = node[args[i]]
			if(typeof node == "undefined")
				continue
			desc = node["DESC"] ? node["DESC"] : desc;
	}
	
	if(document.getElementById("acts").value!="train")
		document.getElementById("description").innerText = desc;

	requestToRespondingAction(args);

}



