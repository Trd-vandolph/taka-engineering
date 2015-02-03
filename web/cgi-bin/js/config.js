function tree(linkName, num, cookieName, maxNum) {
	ls = document.getElementById(linkName).style;
	linkLs = document.getElementById(linkName).currentStyle;

	if(ls.display==""){
		ls.display = linkLs.display;
	}

	var cookieValue = getCookie(cookieName);

	if(cookieValue == null){
		var strVale ="";
		for(i=0;i<maxNum;i++){
			strVale = strVale + "0";
		}
		setCookie(cookieName, strVale);
		cookieValue = getCookie(cookieName);
	}else if(cookieValue.length != maxNum){
		var strVale ="";
		for(i=0;i<maxNum;i++){
			strVale = strVale + "0";
		}
		setCookie(cookieName, strVale);
		cookieValue = getCookie(cookieName);
	}

	val1 = "";
	val2 = "";
	if(num==0){
		val1 = cookieValue.substring(0,0);
	}  else {
		val1 = cookieValue.substring(0,num);
	}
	var num2 = 0;
	num2 = eval(num) + 1;
	val2 = cookieValue.substring( num2,cookieValue.length);

	if(ls.display == 'none') {
		ls.display = "block";
		setCookie(cookieName, (val1 + '1' + val2) );
	} else {
		ls.display = "none";
		setCookie(cookieName, (val1 + '0' + val2) );
	}
}

function treeInit(linkName, num, cookieName, maxNum) {
	ls = document.getElementById(linkName).style;
	linkLs = document.getElementById(linkName).currentStyle;

	if(ls.display==""){
		ls.display = linkLs.display;
	}

	var cookieValue = getCookie(cookieName);

	if(cookieValue == null){
		var strVale ="";
		for(i=0;i<maxNum;i++){
			strVale = strVale + "1";
		}
		setCookie(cookieName, strVale);
		cookieValue = getCookie(cookieName);
	}else if(cookieValue.length != maxNum){
		var strVale ="";
		for(i=0;i<maxNum;i++){
			strVale = strVale + "1";
		}
		setCookie(cookieName, strVale);
		cookieValue = getCookie(cookieName);
	}

	val1 = cookieValue.substring(num,num+1);

	if(val1 == '1') {
		ls.display = "block";
	} else {
		ls.display = "none";
	}
}

function plTreeAllSet() {
	for(i=0;i<plMaxNum;i++){
		treeInit((plLinkName + i), i, plCookieName, plMaxNum);
	}
}

function ilTreeAllSet() {
	for(i=0;i<ilMaxNum;i++){
		treeInit((ilLinkName + i), i, ilCookieName, ilMaxNum);
	}
}

function view(LinkName) {
	ls = document.getElementById(LinkName).style;
	linkLs = document.getElementById(LinkName).currentStyle;

	if(ls.display==""){
		ls.display = linkLs.display;
	}

	if(ls.display == 'none') {
		ls.display = "block";
	} else {
		ls.display = "none";
	}
}

imgElement = new Array();
imgElement[ 0 ] = document.createElement('img');
imgElement[ 1 ] = document.createElement('img');
imgElement[ 2 ] = document.createElement('img');

elementName = new Array();
elementName[ 0 ]=new Array("main");
elementName[ 1 ]=new Array("sub1");
elementName[ 2 ]=new Array("sub2");

imgLoadingLfg = new Array();
imgLoadingLfg[ 0 ] = false;
imgLoadingLfg[ 1 ] = false;
imgLoadingLfg[ 2 ] = false;
imgLoadingLfg[ 3 ] = false;

function changeImage(num){
	if (!document.createElement || !document.getElementById) return;
	document.getElementById("imgs").src =  main_img[num];
	n = num;

	imgLoadingLfg[ 3 ] = true;

	var Img = document.createElement('img');
	Img.style.border="0px";
	Img.src = main_img[ num ];
	Img.id="view";

	var w = Img.width;
	var h = Img.height;

	if( w >= h && w > 300) {
		var h_ = w / 300;
		Img.style.width = "300px";
		Img.style.height = (h / h_) + "px";
	}else if( h >= w && h > 300) {
		var w_ = h / 300;
		Img.style.height = "300px";
		Img.style.width = (w / w_) + "px";
	}

	if(document.getElementById("imgs").firstChild != null){
		document.getElementById("imgs").removeChild(document.getElementById("imgs").firstChild);
	}
	document.getElementById("imgs").appendChild(Img);
}

function appendImgs() {
	if (!document.createElement || !document.getElementById) return;
	
	var Img = document.createElement('img');
	Img.style.border="0px";
	Img.src = main_img[ 0 ];

	var w = Img.width;
	var h = Img.height;
	
	if( w >= h && w > 300) {
		var h_ = w / 300;
		Img.style.width = "300px";
		Img.style.height = (h / h_) + "px";
	}else if( h >= w && h > 300) {
		var w_ = h / 300;
		Img.style.height = "300px";
		Img.style.width = (w / w_) + "px";
	}

	if(document.getElementById("imgs").firstChild != null){
		document.getElementById("imgs").removeChild(document.getElementById("imgs").firstChild);
	}
	document.getElementById("imgs").appendChild(Img);
}

function appendChildImgs(elementById, num) {
	if (!document.createElement || !document.getElementById) return;
	
	var Img = document.createElement('img');
	Img.style.border="0px";
	Img.src=main_img[ num ];

	var w = Img.width;
	var h = Img.height;
	var px = 100;
	var par = 0;

	if (px!=0){
		var h_ = w / px;
		Img.style.width = px + "px";
		Img.style.height = (h / h_) + "px";
	}else {
		var w_ = w * par / 100;
		var h_ = h * par / 100;
		Img.style.width = w_ + "px";
		Img.style.height = h_ + "px";
	}

	document.getElementById(elementById).appendChild(Img);
}

function appendChildImgs2(element, elementById, num) {
	if (!document.createElement || !document.getElementById) return;
	
	element.style.border="0px";

	var w = element.width;
	var h = element.height;
	var px = img_px[ num ];
	var par = img_percent[ num ];
	var unitFlg = img_unitFlg[ num ];

	if (unitFlg==0){
		var h_ = w / px;
		element.style.width = px + "px";
		element.style.height = (h / h_) + "px";
	}else {
		var w_ = w * par / 100;
		var h_ = h * par / 100;
		element.style.width = w_ + "px";
		element.style.height = h_ + "px";
	}

	document.getElementById(elementById).appendChild(element);
}

var imgTimerID;
var checkCount, checkCountMax = 250;

function init()
{
	img=new Image();
	img.src=main_img[ 0 ];


	for(i=0;i<main_img.length;i++){
		imgElement[i].src = main_img[ i ];
	}

	checkCount = 0;
	clearInterval(imgTimerID);
	imgTimerID = setInterval("loadImage()", 200);
}

function loadImage()
{
	checkCount++;
	var flgLoad = true;
	for(i=0;i<main_img.length;i++){
		if (imgElement[i].complete && imgLoadingLfg[i]==false){
			
			imgLoadingLfg[i]=true;
			appendChildImgs2(imgElement[i], elementName[i],i);
			if(i==0 && imgLoadingLfg[3]==false){
				appendImgs();
			}
		}else{
			flgLoad = false;
		}
	}

	if (flgLoad || checkCount > checkCountMax) {
		clearInterval(imgTimerID);
		init2();
	}
}

function init2()
{

	for(i=0;i<main_img.length;i++){
		if (imgLoadingLfg[i]==false){
			appendChildImgs2(imgElement[i], elementName[i],i);
		}
	}
	if(imgLoadingLfg[0]==false || imgLoadingLfg[3]==false){
		appendImgs();
	}
}

slide_imgElement = new Array();
slide_imgElement[ 0 ] = document.createElement('img');
var slideImgTimerID;

function init_slideShow()
{
	for(i=0;i<slide_array.length;i++){
		slide_imgElement[i] = document.createElement('img');
		slide_imgElement[i].src = slide_array[ i ];
	}

	checkCount = 0;
	clearInterval(slideImgTimerID);
	slideImgTimerID = setInterval("loadSlideImage()", 200);
}

function loadSlideImage()
{
	checkCount++;
	var flgLoad = true;
	for(i=0;i<slide_imgElement.length;i++){
		if (slide_imgElement[i].complete){
		}else{
			flgLoad = false;
		}
	}

	if (flgLoad || checkCount > checkCountMax) {
		clearInterval(slideImgTimerID);
		startSlideshow();
	}
}

function startSlideshow()
{
	$('slideshow').innerHTML = "";
	var slideshow = initTimedSlideShow($('slideshow'), slide_array, slideShowDelay);
}

function imgPopUp() {
	if (!document.createElement || !document.getElementById) return;
	var src = document.getElementById("imgs").firstChild.src;
	
	window.open('../imageView.html?img=' + src ,'','scrollbars=yes,location=no,Width=600,Height=600,resizable=yes');
}

function logout()
{
	httpObj = createXMLHttpRequest(displayData3);
	var timestampID = createTimestampID();
	if (httpObj)
	{
		var strURL = "cgi-bin/module_login.cgi?USERNAME=&PASSWORD=&action=logout&" + timestampID;
		if(cgiFlg == 1){
			strURL = "./module_login.cgi?USERNAME=&PASSWORD=&action=logout&" + timestampID;
		}
		httpObj.open("GET",strURL,true);
		httpObj.send(null);
	}
}

function displayData3()
{
	if ((httpObj.readyState == 4) && (httpObj.status == 200))
	{
		$("ms").innerHTML = httpObj.responseText;
	}else{
		$("ms").innerHTML = "<strong>ログアウト中...</strong>";
	}
}

function login()
{
	ID = document.ajaxForm.ID.value;
	PASSWORD = document.ajaxForm.PASSWORD.value;
	action = document.ajaxForm.action.value;
	loginKeep = '';
	if(document.ajaxForm.loginKeep.checked == true) {
		loginKeep = document.ajaxForm.loginKeep.value;
	}

	httpObj = createXMLHttpRequest(displayData2);
	var timestampID = createTimestampID();
	if (httpObj)
	{
		var strURL = "cgi-bin/module_login.cgi?ID="+ID+"&PASSWORD="+PASSWORD+"&loginKeep="+loginKeep+"&action=action&" + timestampID;
		if(cgiFlg == 1){
			strURL = "./module_login.cgi?ID="+ID+"&PASSWORD="+PASSWORD+"&loginKeep="+loginKeep+"&action=action&" + timestampID;
		}
		httpObj.open("GET",strURL,true);
		httpObj.send(null);
	}
}

function displayData2()
{
	if ((httpObj.readyState == 4) && (httpObj.status == 200))
	{
		$("ms").innerHTML = httpObj.responseText;
	}else{
		$("ms").innerHTML = "<strong>認証中...</strong>";
	}
}

function onLoadLogin()
{
	httpObj = createXMLHttpRequest(displayData);
	var timestampID = createTimestampID();
	if (httpObj)
	{
		var strURL = "cgi-bin/module_login.cgi?USERNAME=&PASSWORD=&action=load&" + timestampID;
		if(cgiFlg == 1){
			strURL = "./module_login.cgi?USERNAME=&PASSWORD=&action=load&" + timestampID;
		}
		httpObj.open("GET",strURL,true);
		httpObj.send(null);
	}
}

function displayData()
{
	if ((httpObj.readyState == 4) && (httpObj.status == 200))
	{
		$("ms").innerHTML = httpObj.responseText;
	}else{
		$("ms").innerHTML = "<strong>Wait...</strong><br>";
	}
}

function setCookie(myCookie,myValue){
	if (cookieEnabledFlg == 1) {
		myItem = "@" + myCookie + "=" + escape(myValue) + ";";
		document.cookie =  myItem
	}
}

function getCookie(myCookie){
	if (cookieEnabledFlg == 1) {
		myCookie = "@" + myCookie + "=";
		myValue = null;
		myStr = document.cookie + ";" ;
		myOfst = myStr.indexOf(myCookie);
		if (myOfst != -1){
			myStart = myOfst + myCookie.length;
			myEnd   = myStr.indexOf(";" , myStart);
			myValue = unescape(myStr.substring(myStart,myEnd));
		}
	} else {
		myValue = '';
	}
	return myValue;
}

function getLoginCookie(myCookie){
	if (cookieEnabledFlg == 1) {
		myCookie = myCookie + "=";
		myValue = null;
		myStr = document.cookie + ";" ;
		myOfst = myStr.indexOf(myCookie);
		if (myOfst != -1){
			myStart = myOfst + myCookie.length + 1;
			myEnd   = myStr.indexOf(";" , myStart);
			myValue = unescape(myStr.substring(myStart,myEnd));
		}
	} else {
		myValue = '';
	}
	return myValue;
}

function createTimestampID(){
	return "TimestampID=" +(new Date()).getTime();
}

function login_jump(str_url) {
	var form = window.document.createElement("form");
	form.action= str_url;
	form.method ="POST";

	var cookie_id = getLoginCookie("ID");
	var cookie_passwoed = getLoginCookie("PASSWORD");
	var cookie_login_status = getLoginCookie("LOGIN_STATUS");
	if(cookie_id == null) cookie_id = '';
	if(cookie_passwoed == null) cookie_passwoed = '';
	if(cookie_login_status == null) cookie_login_status = '';

	var input_id = window.document.createElement("input");
	input_id.type = "hidden";
	input_id.name = "ID";
	input_id.value = cookie_id;

	var input_pass = window.document.createElement("input");
	input_pass.type = "hidden";
	input_pass.name = "PASSWORD";
	input_pass.value = cookie_passwoed;

	var input_status = window.document.createElement("input");
	input_status.type = "hidden";
	input_status.name = "loginKeep";
	input_status.value = cookie_login_status;

	form.appendChild(input_id);
	form.appendChild(input_pass);
	form.appendChild(input_status);

	window.document.appendChild(form);

	form.submit();
}

var doChkFlg = false;
function doChk() {
	if (doChkFlg) {
		return false;
	} else {
		doChkFlg = true;
		return true;
	}
}

function btnPost(control, url) {
	
	// 全てのFormを取得する。
	var all_forms = document.forms;
	
	// ボタンの2重押下防止
	if ( control != false ) {
		for ( var i = 0; i < all_forms.length; i++ ) {
			var elements = document.forms[i].elements;
			for ( var j = 0; j < elements.length; j++ ) {
				if ( elements[j].type == 'button' || elements[j].type == 'submit') {
					elements[j].disabled = true;
				}
			}
		}
	}
	
	location.href = url;
}

function btnPost2(control) {
	
	// 全てのFormを取得する。
	var all_forms = document.forms;
	
	// ボタンの2重押下防止
	if ( control != false ) {
		for ( var i = 0; i < all_forms.length; i++ ) {
			var elements = document.forms[i].elements;
			for ( var j = 0; j < elements.length; j++ ) {
				if ( elements[j].type == 'button' || elements[j].type == 'submit') {
					elements[j].disabled = true;
				}
			}
		}
	}
}
