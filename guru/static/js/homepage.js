function showaccount(){
	visibility = document.getElementById('account').style.display
	if(visibility=='none'){
	document.getElementById('account').style.display='block';
	}
	else{
	document.getElementById('account').style.display='none';
	}
}

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  this.style.display="None";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  this.style.display="block";
}
function createclassform(){
	if (document.getElementById('classform').style.display=='none'){
	document.getElementById('joinform').style.display='none';
	document.getElementById('classform').style.display='block';			
	}
	else{
		document.getElementById('classform').style.display='none'
	}
}
function joinform(){
if (document.getElementById('joinform').style.display=='none'){
document.getElementById('classform').style.display='none'
document.getElementById('joinform').style.display='block';		
}
else{
	document.getElementById('joinform').style.display='none';
}
}