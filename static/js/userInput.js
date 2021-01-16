function getTextInput(){return document.getElementById("input").value;}
function predLoc(){
	return document.getElementById("prediction");
}
function getInput(text,default_val=0.2,min_val=0.01,max_val=0.99){
	do{
		var value = prompt(text,default_val);
		if(value==null)
		  return 

		if (value != parseFloat(value, 10) || value <=min_val || value >=max_val)
		  alert("0.01 ve 0.99 arasında bir sayı girin.");
	  
	}while(value != parseFloat(value, 10) || value <=min_val || value >=max_val);

	return parseFloat(value);
  
}

function handleDrag(event){
	event.preventDefault();
	document.getElementById("myDropzone").style.zIndex="100";
	document.getElementById("myDropzone").style.opacity="0.5";
}
function handleDrop(event){
	document.getElementById("myDropzone").style.zIndex="-1";
	document.getElementById("myDropzone").style.opacity="0";
}
document.getElementById("myDropzone").addEventListener('ondragstart', handleDrag);
document.getElementById("myDropzone").addEventListener('drag', handleDrag);
document.getElementById("myDropzone").addEventListener('ondragend', handleDrop);
document.getElementById("myDropzone").addEventListener('drop', handleDrop);