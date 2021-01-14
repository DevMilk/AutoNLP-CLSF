
var action = document.getElementById("acts");

function deleteParamForm(){
	if(document.getElementById("form"))
		document.getElementById("form").remove();
}
function callOnMethodChange(){
	let endpoint = document.getElementById("acts").value;
	if(endpoint=="split")
		requestToRespondingAction([]);
	else{
		deleteParamForm();
	}
}

function wait() {
  return new Promise(resolve => {
    resolve();
  });
}

function writeToPredictionElement(responseArray){
	predLoc().innerText=responseArray[0].toUpperCase();
}
var currentArgs;
async function destroyAndReturn(){


	request = {"args": currentArgs,"params":null}
	let formElement = document.getElementById("form");
	let inputs = formElement.getElementsByTagName("input");
	let obj = {}
	for(let i=0;i<inputs.length;i++)
		if(inputs[i].value!="null"){
			let parsed = parseFloat(inputs[i].value); 
			obj[inputs[i].name] = isNaN(parsed) ? inputs[i].value  : parsed;
		}
	request["params"] = obj;

	predLoc().innerText = "Training..."
	await wait();
	POST("/train",request,writeToPredictionElement)
	deleteParamForm();
}

//Ask for parameters before training
function askForParams(paramSet){
	let currentParams = paramSet[0]

	function createInput(name,value){
		return '<label for="'+name+'">'+name+'</label><br> \
    	<input type="text" id="'+name+'" name="'+name+'" value = "'+value+'"><br> '
	}

	let start = '<div id="form" >';
	let end = '<button onclick="destroyAndReturn();">send</button> </div>';
	for(let key in currentParams) 
  			start+=createInput(key,currentParams[key]);
	
	start+=end;
	document.getElementById("parameters").innerHTML =start;
	document.getElementById("form").focus();
}


async function requestToRespondingAction(args){


	let endpoint = document.getElementById("acts").value;

	let request = {
		"text": getTextInput(),
		"args": args,
	}

	if(endpoint=="train"){
		currentArgs = args
		predLoc().innerText = "Enter parameters"
		await wait();
		POST("/"+"param",request,askForParams)
		return;
	}
	if(endpoint=="split"){
		test_ratio = getInput("Enter test ratio");
		if(test_ratio==null || test_ratio ==="undefined")
			return
		request = {"test_ratio": test_ratio}
	}

	predLoc().innerText = (endpoint+"ing...").toUpperCase()
	await wait();
	endpoint = endpoint.toLowerCase()
	POST("/"+endpoint,request,writeToPredictionElement)

}

function getArgFromElement(element){
	return element.innerText.split("\n")[0];
}
function getTag(element){
	return element.getElementsByTagName("a")[0];
}
function getParent(element){
	return element.parentNode;
}
async function elementHiden(element){
	element.style.visibility = element.style.visibility == "hidden" ? "visible": "hidden";
	await wait();
}


function click(event){

	currentElement = event.target; 
	current =  getArgFromElement(currentElement);
	args = [current];

	while(current!="ALL IN ONE" && currentElement!=null){
		if(currentElement.tagName=="MENUITEM" && !args.includes(current))
			args.push(current);
		currentElement = getParent(currentElement);
		current = getArgFromElement(currentElement);
	}


	let argsArray = []
	let node = JSON.parse(JSON.stringify(model_tree))
	if(args.length!=0){
		for(var i = 0;i<args.length;i++){
			argsArray.push(args[i])

		}
	}
	let desc = ""
	for(var i = args.length-1;i>=0;i--){
			console.log(node,args[i])
			node = node[args[i]]
			desc = node["DESC"] ? node["DESC"] : desc;
	}
	
	document.getElementById("description").innerText = desc;

	requestToRespondingAction(argsArray);



}



