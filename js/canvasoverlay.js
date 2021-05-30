// https://github.com/joshua-gould/OpenSeadragonCanvasOverlayHd v1.0.0 Copyright 2018 Joshua Gould
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?module.exports=t():"function"==typeof define&&define.amd?define(t):(e.OpenSeadragon=e.OpenSeadragon||{},e.OpenSeadragon.CanvasOverlayHd=t())}(this,function(){"use strict";return class{constructor(e,t){this._viewer=e,this.backingScale=1,this._containerWidth=0,this._containerHeight=0,this._canvasdiv=document.createElement("div"),this._canvasdiv.style.position="absolute",this._canvasdiv.style.left=0,this._canvasdiv.style.top=0,this._canvasdiv.style.width="100%",this._canvasdiv.style.height="100%",this._viewer.canvas.appendChild(this._canvasdiv),this._canvas=document.createElement("canvas"),this._canvasdiv.appendChild(this._canvas),this.onRedraw=t.onRedraw||function(){},this.clearBeforeRedraw=void 0===t.clearBeforeRedraw||t.clearBeforeRedraw,this._viewer.addHandler("update-viewport",()=>{this.resize(),this._updateCanvas()}),this._viewer.addHandler("open",()=>{this.resize(),this._updateCanvas()})}static getTileIndexFromPixel(e,t){let i=e.viewport.pointFromPixel(t);for(let t=0,a=e.world.getItemCount();t<a;t++){let a=e.world.getItemAt(t),n=new OpenSeadragon.Rect(i.x,i.y,0,0),s=a._viewportToTiledImageRectangle(n).getTopLeft(),r=a.source;if(s.x>=0&&s.x<=1&&s.y>=0&&s.y<=1/r.aspectRatio)return t}return-1}canvas(){return this._canvas}context2d(){return this._canvas.getContext("2d")}clear(){this._canvas.getContext("2d").clearRect(0,0,this._containerWidth*this.backingScale,this._containerHeight*this.backingScale)}resize(){let e=1;"undefined"!=typeof window&&"devicePixelRatio"in window&&window.devicePixelRatio>1&&(e=window.devicePixelRatio);let t=this.backingScale!==e;this.backingScale=e,(this._containerWidth!==this._viewer.container.clientWidth||t)&&(this._containerWidth=this._viewer.container.clientWidth,this._canvasdiv.setAttribute("width",e*this._containerWidth),this._canvas.setAttribute("width",e*this._containerWidth),this._canvas.style.width=this._containerWidth+"px"),(this._containerHeight!==this._viewer.container.clientHeight||t)&&(this._containerHeight=this._viewer.container.clientHeight,this._canvasdiv.setAttribute("height",e*this._containerHeight),this._canvas.setAttribute("height",e*this._containerHeight),this._canvas.style.height=this._containerHeight+"px")}_updateCanvas(){let e=this._viewer.viewport.getZoom(!0);this.clearBeforeRedraw&&this.clear();let t=this._canvas.getContext("2d");for(let i=0,a=this._viewer.world.getItemCount();i<a;i++){let a=this._viewer.world.getItemAt(i);if(a){let n=a.viewportToImageZoom(e),s=a.imageToViewportCoordinates(0,0,!0),r=this._viewer.viewport.pixelFromPoint(s,!0);t.scale(this.backingScale,this.backingScale),t.translate(r.x,r.y),t.scale(n,n),this.onRedraw({index:i,context:t,x:r.x,y:r.y,zoom:n}),t.setTransform(1,0,0,1,0,0)}}}}});
