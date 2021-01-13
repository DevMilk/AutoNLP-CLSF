
var action = document.getElementById("acts");

var desc = {
	"BOW": "IN THIS MODEL, A TEXT (SUCH AS A SENTENCE OR A DOCUMENT) IS \
	REPRESENTED AS THE BAG (MULTISET) OF ITS WORDS, DISREGARDING GRAMMAR AND EVEN WORD ORDER BUT KEEPING MULTIPLICITY."
}


function deleteParamForm(){
	if(document.getElementById("form"))
		document.getElementById("form").remove();
}
function callIfSplit(){
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

var currentArgs;
async function destroyAndReturn(){


	request = {"args": currentArgs,"params":null}
	let formElement = document.getElementById("form");
	let inputs = formElement.getElementsByTagName("input");
	let obj = {}
	for(let i=0;i<inputs.length;i++)
		if(inputs[i].value!="null")
			obj[inputs[i].name] = parseFloat(inputs[i].value)
	request["params"] = obj;

	predLoc().innerText = "Training..."
	await wait();
	POST("/train",request,function(responseArray){predLoc().innerText=responseArray[0];})
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
		if(parseFloat(currentParams[key])|| currentParams[key]==0)
  			start+=createInput(key,currentParams[key]);
	
	start+=end;
	document.getElementById("parameters").innerHTML =start;
	document.getElementById("form").focus();
}


async function requestToRespondingAction(args){


	let endpoint = document.getElementById("acts").value;
	predLoc().innerText = (endpoint+"ing...").toUpperCase()
	await wait();

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
		request = {"test_ratio": test_ratio}
	}
	endpoint = endpoint.toLowerCase()
	console.log(request)
	POST("/"+endpoint,request,function(responseArray){predLoc().innerText=responseArray[0];})

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

let descriptionLoc = document.getElementById("description");

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
	if(args.length!=0){
		for(var i = 0;i<args.length;i++){
			argsArray.push(args[i])
		}
	}


	requestToRespondingAction(argsArray);



}



