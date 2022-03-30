
/*
 Highcharts JS v9.3.3 (2022-02-01)

 Exporting module

 (c) 2010-2021 Torstein Honsi

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/export-data",["highcharts","highcharts/modules/exporting"],function(k){a(k);a.Highcharts=k;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function k(a,f,d,p){a.hasOwnProperty(f)||(a[f]=p.apply(null,d))}a=a?a._modules:{};k(a,"Extensions/DownloadURL.js",[a["Core/Globals.js"]],function(a){var f=a.isSafari,
    d=a.win,p=d.document,l=d.URL||d.webkitURL||d,r=a.dataURLtoBlob=function(a){if((a=a.replace(/filename=.*;/,"").match(/data:([^;]*)(;base64)?,([0-9A-Za-z+/]+)/))&&3<a.length&&d.atob&&d.ArrayBuffer&&d.Uint8Array&&d.Blob&&l.createObjectURL){var f=d.atob(a[3]),m=new d.ArrayBuffer(f.length);m=new d.Uint8Array(m);for(var b=0;b<m.length;++b)m[b]=f.charCodeAt(b);a=new d.Blob([m],{type:a[1]});return l.createObjectURL(a)}};a=a.downloadURL=function(a,l){var m=d.navigator,b=p.createElement("a");if("string"===
    typeof a||a instanceof String||!m.msSaveOrOpenBlob){a=""+a;m=/Edge\/\d+/.test(m.userAgent);if(f&&"string"===typeof a&&0===a.indexOf("data:application/pdf")||m||2E6<a.length)if(a=r(a)||"",!a)throw Error("Failed to convert to blob");if("undefined"!==typeof b.download)b.href=a,b.download=l,p.body.appendChild(b),b.click(),p.body.removeChild(b);else try{var g=d.open(a,"chart");if("undefined"===typeof g||null===g)throw Error("Failed to open window");}catch(E){d.location.href=a}}else m.msSaveOrOpenBlob(a,
    l)};return{dataURLtoBlob:r,downloadURL:a}});k(a,"Extensions/ExportData.js",[a["Core/Axis/Axis.js"],a["Core/Chart/Chart.js"],a["Core/Renderer/HTML/AST.js"],a["Core/Globals.js"],a["Core/DefaultOptions.js"],a["Core/Utilities.js"],a["Extensions/DownloadURL.js"]],function(a,f,d,p,l,r,m){function k(a,n){var c=g.navigator,b=-1<c.userAgent.indexOf("WebKit")&&0>c.userAgent.indexOf("Chrome"),d=g.URL||g.webkitURL||g;try{if(c.msSaveOrOpenBlob&&g.MSBlobBuilder){var t=new g.MSBlobBuilder;t.append(a);return t.getBlob("image/svg+xml")}if(!b)return d.createObjectURL(new g.Blob(["\ufeff"+
    a],{type:n}))}catch(N){}}var I=p.doc,b=p.seriesTypes,g=p.win;p=l.getOptions;l=l.setOptions;var E=r.addEvent,J=r.defined,F=r.extend,K=r.find,C=r.fireEvent,L=r.isNumber,v=r.pick,G=m.downloadURL;l({exporting:{csv:{annotations:{itemDelimiter:"; ",join:!1},columnHeaderFormatter:null,dateFormat:"%Y-%m-%d %H:%M:%S",decimalPoint:null,itemDelimiter:null,lineDelimiter:"\n"},showTable:!1,useMultiLevelHeaders:!0,useRowspanHeaders:!0},lang:{downloadCSV:"Download CSV",downloadXLS:"Download XLS",exportData:{annotationHeader:"Annotations",
    categoryHeader:"Category",categoryDatetimeHeader:"DateTime"},viewData:"View data table",hideData:"Hide data table"}});E(f,"render",function(){this.options&&this.options.exporting&&this.options.exporting.showTable&&!this.options.chart.forExport&&!this.dataTableDiv&&this.viewData()});f.prototype.setUpKeyToAxis=function(){b.arearange&&(b.arearange.prototype.keyToAxis={low:"y",high:"y"});b.gantt&&(b.gantt.prototype.keyToAxis={start:"x",end:"x"})};f.prototype.getDataRows=function(c){var n=this.hasParallelCoordinates,
    y=this.time,b=this.options.exporting&&this.options.exporting.csv||{},d=this.xAxis,t={},f=[],m=[],p=[],z;var g=this.options.lang.exportData;var l=g.categoryHeader,M=g.categoryDatetimeHeader,w=function(q,e,d){if(b.columnHeaderFormatter){var n=b.columnHeaderFormatter(q,e,d);if(!1!==n)return n}return q?q instanceof a?q.options.title&&q.options.title.text||(q.dateTime?M:l):c?{columnTitle:1<d?e:q.name,topLevelColumnTitle:q.name}:q.name+(1<d?" ("+e+")":""):l},H=function(a,c,e){var q={},d={};c.forEach(function(c){var b=
    (a.keyToAxis&&a.keyToAxis[c]||c)+"Axis";b=L(e)?a.chart[b][e]:a[b];q[c]=b&&b.categories||[];d[c]=b&&b.dateTime});return{categoryMap:q,dateTimeValueAxisMap:d}},r=function(a,c){return a.data.filter(function(a){return"undefined"!==typeof a.y&&a.name}).length&&c&&!c.categories&&!a.keyToAxis?a.pointArrayMap&&a.pointArrayMap.filter(function(a){return"x"===a}).length?(a.pointArrayMap.unshift("x"),a.pointArrayMap):["x","y"]:a.pointArrayMap||["y"]},h=[];var x=0;this.setUpKeyToAxis();this.series.forEach(function(a){var e=
    a.xAxis,q=a.options.keys||r(a,e),f=q.length,g=!a.requireSorting&&{},k=d.indexOf(e),B=H(a,q),l;if(!1!==a.options.includeInDataExport&&!a.options.isInternal&&!1!==a.visible){K(h,function(a){return a[0]===k})||h.push([k,x]);for(l=0;l<f;)z=w(a,q[l],q.length),p.push(z.columnTitle||z),c&&m.push(z.topLevelColumnTitle||z),l++;var A={chart:a.chart,autoIncrement:a.autoIncrement,options:a.options,pointArrayMap:a.pointArrayMap};a.options.data.forEach(function(c,d){n&&(B=H(a,q,d));var w={series:A};a.pointClass.prototype.applyOptions.apply(w,
    [c]);c=w.x;var h=a.data[d]&&a.data[d].name;l=0;if(!e||"name"===a.exportKey||!n&&e&&e.hasNames&&h)c=h;g&&(g[c]&&(c+="|"+d),g[c]=!0);t[c]||(t[c]=[],t[c].xValues=[]);t[c].x=w.x;t[c].name=h;for(t[c].xValues[k]=w.x;l<f;)d=q[l],h=w[d],t[c][x+l]=v(B.categoryMap[d][h],B.dateTimeValueAxisMap[d]?y.dateFormat(b.dateFormat,h):null,h),l++});x+=l}});for(e in t)Object.hasOwnProperty.call(t,e)&&f.push(t[e]);var e=c?[m,p]:[p];for(x=h.length;x--;){var A=h[x][0];var D=h[x][1];var k=d[A];f.sort(function(a,c){return a.xValues[A]-
    c.xValues[A]});g=w(k);e[0].splice(D,0,g);c&&e[1]&&e[1].splice(D,0,g);f.forEach(function(a){var c=a.name;k&&!J(c)&&(k.dateTime?(a.x instanceof Date&&(a.x=a.x.getTime()),c=y.dateFormat(b.dateFormat,a.x)):c=k.categories?v(k.names[a.x],k.categories[a.x],a.x):a.x);a.splice(D,0,c)})}e=e.concat(f);C(this,"exportData",{dataRows:e});return e};f.prototype.getCSV=function(a){var c="",d=this.getDataRows(),b=this.options.exporting.csv,f=v(b.decimalPoint,","!==b.itemDelimiter&&a?(1.1).toLocaleString()[1]:"."),
    l=v(b.itemDelimiter,","===f?";":","),g=b.lineDelimiter;d.forEach(function(a,b){for(var n,y=a.length;y--;)n=a[y],"string"===typeof n&&(n='"'+n+'"'),"number"===typeof n&&"."!==f&&(n=n.toString().replace(".",f)),a[y]=n;c+=a.join(l);b<d.length-1&&(c+=g)});return c};f.prototype.getTable=function(a){var c=function(a){if(!a.tagName||"#text"===a.tagName)return a.textContent||"";var d=a.attributes,b="<"+a.tagName;d&&Object.keys(d).forEach(function(a){b+=" "+a+'="'+d[a]+'"'});b+=">";b+=a.textContent||"";(a.children||
    []).forEach(function(a){b+=c(a)});return b+="</"+a.tagName+">"};a=this.getTableAST(a);return c(a)};f.prototype.getTableAST=function(a){var c=0,b=[],d=this.options,f=a?(1.1).toLocaleString()[1]:".",l=v(d.exporting.useMultiLevelHeaders,!0);a=this.getDataRows(l);var g=l?a.shift():null,k=a.shift(),m=function(a,c,b,d){var h=v(d,"");c="text"+(c?" "+c:"");"number"===typeof h?(h=h.toString(),","===f&&(h=h.replace(".",f)),c="number"):d||(c="empty");b=F({"class":c},b);return{tagName:a,attributes:b,textContent:h}};
    !1!==d.exporting.tableCaption&&b.push({tagName:"caption",attributes:{"class":"highcharts-table-caption"},textContent:v(d.exporting.tableCaption,d.title.text?d.title.text:"Chart")});for(var p=0,r=a.length;p<r;++p)a[p].length>c&&(c=a[p].length);b.push(function(a,c,b){var f=[],h=0;b=b||c&&c.length;var n=0,e;if(e=l&&a&&c){a:if(e=a.length,c.length===e){for(;e--;)if(a[e]!==c[e]){e=!1;break a}e=!0}else e=!1;e=!e}if(e){for(e=[];h<b;++h){var g=a[h];var k=a[h+1];g===k?++n:n?(e.push(m("th","highcharts-table-topheading",
    {scope:"col",colspan:n+1},g)),n=0):(g===c[h]?d.exporting.useRowspanHeaders?(k=2,delete c[h]):(k=1,c[h]=""):k=1,g=m("th","highcharts-table-topheading",{scope:"col"},g),1<k&&g.attributes&&(g.attributes.valign="top",g.attributes.rowspan=k),e.push(g))}f.push({tagName:"tr",children:e})}if(c){e=[];h=0;for(b=c.length;h<b;++h)"undefined"!==typeof c[h]&&e.push(m("th",null,{scope:"col"},c[h]));f.push({tagName:"tr",children:e})}return{tagName:"thead",children:f}}(g,k,Math.max(c,k.length)));var u=[];a.forEach(function(a){for(var b=
    [],d=0;d<c;d++)b.push(m(d?"td":"th",null,d?{}:{scope:"row"},a[d]));u.push({tagName:"tr",children:b})});b.push({tagName:"tbody",children:u});b={tree:{tagName:"table",id:"highcharts-data-table-"+this.index,children:b}};C(this,"aftergetTableAST",b);return b.tree};f.prototype.downloadCSV=function(){var a=this.getCSV(!0);G(k(a,"text/csv")||"data:text/csv,\ufeff"+encodeURIComponent(a),this.getFilename()+".csv")};f.prototype.downloadXLS=function(){var a='<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head>\x3c!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>Ark1</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--\x3e<style>td{border:none;font-family: Calibri, sans-serif;} .number{mso-number-format:"0.00";} .text{ mso-number-format:"@";}</style><meta name=ProgId content=Excel.Sheet><meta charset=UTF-8></head><body>'+
    this.getTable(!0)+"</body></html>";G(k(a,"application/vnd.ms-excel")||"data:application/vnd.ms-excel;base64,"+g.btoa(unescape(encodeURIComponent(a))),this.getFilename()+".xls")};f.prototype.viewData=function(){this.toggleDataTable(!0)};f.prototype.hideData=function(){this.toggleDataTable(!1)};f.prototype.toggleDataTable=function(a){(a=v(a,!this.isDataTableVisible))&&!this.dataTableDiv&&(this.dataTableDiv=I.createElement("div"),this.dataTableDiv.className="highcharts-data-table",this.renderTo.parentNode.insertBefore(this.dataTableDiv,
    this.renderTo.nextSibling));this.dataTableDiv&&(this.dataTableDiv.style.display=a?"block":"none",a&&(this.dataTableDiv.innerHTML=d.emptyHTML,(new d([this.getTableAST()])).addToDOM(this.dataTableDiv),C(this,"afterViewData",this.dataTableDiv)));this.isDataTableVisible=a;a=this.exportDivElements;var b=this.options.exporting,c=b&&b.buttons&&b.buttons.contextButton.menuItems;b=this.options.lang;u&&u.menuItemDefinitions&&b&&b.viewData&&b.hideData&&c&&a&&(a=a[c.indexOf("viewData")])&&d.setElementHTML(a,
    this.isDataTableVisible?b.hideData:b.viewData)};var u=p().exporting;u&&(F(u.menuItemDefinitions,{downloadCSV:{textKey:"downloadCSV",onclick:function(){this.downloadCSV()}},downloadXLS:{textKey:"downloadXLS",onclick:function(){this.downloadXLS()}},viewData:{textKey:"viewData",onclick:function(){this.toggleDataTable()}}}),u.buttons&&u.buttons.contextButton.menuItems.push("separator","downloadCSV","downloadXLS","viewData"));b.map&&(b.map.prototype.exportKey="name");b.mapbubble&&(b.mapbubble.prototype.exportKey=
    "name");b.treemap&&(b.treemap.prototype.exportKey="name")});k(a,"masters/modules/export-data.src.js",[],function(){})});
    //# sourceMappingURL=export-data.js.map 