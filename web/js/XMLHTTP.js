// HTTPí êMópÅAã§í ä÷êî
function createXMLHttpRequest(cbFunc)
{
	var XMLhttpObject = null;
	try{
		XMLhttpObject = new XMLHttpRequest();
	}catch(e){
		try{
			XMLhttpObject = new ActiveXObject("Msxml2.XMLHTTP");
		}catch(e){
			try{
				XMLhttpObject = new ActiveXObject("Microsoft.XMLHTTP");
			}catch(e){
				return null;
			}
		}
	}
	if (XMLhttpObject){
		if(cbFunc) XMLhttpObject.onreadystatechange = cbFunc;
	}
	return XMLhttpObject;
}

// document.getElementById
function $(tagId)
{
	return document.getElementById(tagId);
}
