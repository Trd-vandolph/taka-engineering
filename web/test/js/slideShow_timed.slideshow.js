/*
    This file is part of JonDesign's SmoothSlideshow v2.0.

    JonDesign's SmoothSlideshow is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    JonDesign's SmoothSlideshow is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

    Main Developer: Jonathan Schemoul (JonDesign: http://www.jondesign.net/)
    Contributed code by:
    - Christian Ehret (bugfix)
    - Simon Willison (addLoadEvent)
*/

var timedSlideShow = Class.create();


// 画像が1枚の場合2枚に変更
if (slide_array.length == 1){
	slide_array[1] = slide_array[0];
}

// implementing the class
timedSlideShow.prototype = {
	initialize: function(element, data,slideShowDelay) {
		this.currentIter = 0;
		this.lastIter = 0;
		this.maxIter = 0;
		this.slideShowElement = element;
		this.slideShowData = data;
		this.slideShowInit = 1;
		this.slideElements = Array();
		this.slideShowDelay = slideShowDelay;
		this.articleLink = "";



//		alert('クラス初期化:slideShowDelay='+slideShowDelay);
//	_sleep(1000);


		element.style.display="block";

		this.articleLink = document.createElement('a');
		this.articleLink.className = 'global';
		element.appendChild(this.articleLink);
		//this.articleLink.href = "";


		this.maxIter = data.length;
		for(i=0;i<data.length;i++)
		{
			var Img = document.createElement('img');
			Img.className = "slideElement";
			Img.style.position="absolute";
			//currentImg.style.left="0px";
			//currentImg.style.top="0px";
			//currentImg.style.margin="0px";
			Img.style.border="0px";
			Img.src="" + data[i][0] + "";

			var w = Img.width;
			var h = Img.height;

			// 縦横比計算
			if( w >= h && w > 140) {
				var h_ = w / 140;
				Img.style.width = "140px";
				Img.style.height = (h / h_) + "px";
			}else if( h >= w && h > 140) {
				var w_ = h / 140;
				Img.style.height = "140px";
				Img.style.width = (w / w_) + "px";
			}

			this.articleLink.appendChild(Img);
			Img.currentOpacity = new fx.Opacity(Img, {duration: 400});
			Img.setStyle('opacity',0);
			this.slideElements[parseInt(i)] = Img;
		}
		

		if(this.loadFlg != 0){
			this.loadFlg = 0;
		}





		this.loadingElement = document.createElement('div');
		this.loadingElement.className = 'loadingElement';
		this.articleLink.appendChild(this.loadingElement);
		
		this.doSlideShow();
	},
	destroySlideShow: function(element) {
		var myClassName = element.className;
		var newElement = document.createElement('div');
		newElement.className = myClassName;
		element.parentNode.replaceChild(newElement, element);
	},
	startSlideShow: function() {
		this.loadingElement.style.display = "none";
		this.lastIter = this.maxIter - 1;
		this.currentIter = 0;
		this.slideShowInit = 0;
		this.slideElements[parseInt(this.currentIter)].setStyle('opacity', 1);

		setTimeout(this.showInfoSlideShow.bind(this),1000);
		setTimeout(this.hideInfoSlideShow.bind(this),this.slideShowDelay-1000);
		setTimeout(this.nextSlideShow.bind(this),this.slideShowDelay);
	},
	nextSlideShow: function() {
		this.lastIter = this.currentIter;
		this.currentIter++;
		if (this.currentIter >= this.maxIter)
		{
			this.currentIter = 0;
			this.lastIter = this.maxIter - 1;
		}
		this.slideShowInit = 0;
		this.doSlideShow.bind(this)();
	},
	doSlideShow: function() {
		if (this.slideShowInit == 1)
		{
			imgPreloader = new Image();
			// once image is preloaded, start slideshow
			imgPreloader.onload=function(){
				setTimeout(this.startSlideShow.bind(this),10);
			}.bind(this);
			imgPreloader.src = this.slideShowData[0][0];
		} else {
			if (this.currentIter != 0) {
				this.slideElements[parseInt(this.currentIter)].currentOpacity.options.onComplete = function() {
					this.slideElements[parseInt(this.lastIter)].setStyle('opacity',0);
				}.bind(this);
				this.slideElements[parseInt(this.currentIter)].currentOpacity.custom(0, 1);
			} else {
				this.slideElements[parseInt(this.currentIter)].setStyle('opacity',1);
				this.slideElements[parseInt(this.lastIter)].currentOpacity.custom(1, 0);
			}
			setTimeout(this.showInfoSlideShow.bind(this),1000);
			setTimeout(this.hideInfoSlideShow.bind(this),this.slideShowDelay-1000);
			setTimeout(this.nextSlideShow.bind(this),this.slideShowDelay);
		}
	},
	showInfoSlideShow: function() {
	},
	hideInfoSlideShow: function() {
	}
};

function initTimedSlideShow(element, data, time) {
	// 時間
	slideShowDelay = time;
	var slideshow = new timedSlideShow(element, data,time);
	var slideshow1 = Class.create();;
	copy_undef_properties(slideshow, slideshow1);
	
	slideshow1.slideShowDelay = time;

	var divId = "slideshow";
	var baseDiv = document.getElementById(divId).style;
	var baseDiv_ = document.getElementById(divId).currentStyle;

	return slideshow1;
};

function addLoadEvent(func) {
	var oldonload = window.onload;
	if (typeof window.onload != 'function') {
		window.onload = func;
	} else {
		window.onload = function() {
			oldonload();
			func();
		}
	}
}














function copy_undef_properties(src, dest)
{
    for (var prop in src) {
        if (typeof(dest[prop]) == "undefined") { 
            dest[prop] = src[prop];
        }
    }
}



function inherit(subClass, superClass) 
{
    copy_undef_properties(superClass.prototype, subClass.prototype);
}




