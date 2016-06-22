
function printf() {
	 alert('Hello, world');
}


function RemoveBlockquote(strText)
{
var regEx = /<blockquote>(.|\n|\r)*<\/blockquote>/ig;
regEx.multiline=true;
return strText.replace(regEx, "");
}


function RemoveHTML(strText)
{
var regEx = /<[^>]*>/g;
return strText.replace(regEx, "");
}



function CommentQuote(u,b) {


window.location.href=window.location.href+"#report-comment";

string=document.forms["comments_form"].body.value;
string2=ignoreSpaces(RemoveHTML(RemoveBlockquote(document.getElementById(b).innerHTML)));
document.forms["comments_form"].body.value="<blockquote>\n<pre>引用"+u+"的发言：</pre>\n"+string2+"\n</blockquote>\n\n"+string;

return true;
}

function ignoreSpaces(string) {
	var temp = "";
	string = '' + string;
	splitstring = string.split("  "); //双引号之间是个空格；
	for(i = 0; i < splitstring.length; i++)
	temp += splitstring[i];
   return temp;
   }
