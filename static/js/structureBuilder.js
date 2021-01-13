let model_tree = GET("/structure");
const ground = document.getElementById("model-structure");

function createMenu(content,isMain=false){
	let subMenu = '<menu>';
	subMenu += isMain==true ? '<menuitem class="main"><a>ALL IN ONE</a></menuitem>' : '';

	for (let subModel in content){
		subMenu += createModelTree(subModel,content[subModel])
	}
	subMenu+='</menu>'
	return subMenu;
}
function createModelTree(modelName,content){

	let [modelStart,modelEnd] = ['<menuitem><a>'+modelName+'</a>','</menuitem>'];

	//If no other subModel of given model, then return just menuitem
	if(content == [] || typeof content !== 'object' || content == null){
		return modelStart+modelEnd;
	}
	let subMenu = createMenu(content);
	return modelStart+subMenu+modelEnd;

}
ground.innerHTML+=createMenu(model_tree,true);
