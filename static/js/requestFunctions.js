function POST(endpoint, requestBody,handleFunc){
	const xhr = new XMLHttpRequest();   // new HttpRequest instance 
	xhr.open("POST", endpoint);
	xhr.withCredentials = true;
	xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(requestBody));
    xhr.timeout = 0;

    xhr.onreadystatechange = function () {
      if (this.readyState === 4   && 
		  this.status     ==  200 &&
  	      this.status < 300) {
			  if(this.responseText=="")
				  return
			  handleFunc(JSON.parse(this.responseText.replace(/\bNaN\b/g, "null")));
		  }
	  else if(this.status==500){
	  	predLoc().innerText="SERVER ERROR"
	  }
    }
}


function GET(endpoint)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", endpoint, false ); // false for synchronous request
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText.replace(/\bNaN\b/g, "null"));
}