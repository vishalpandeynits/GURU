if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}

function openNav() {
  document.getElementById("mySidenav").style.width = "275px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
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

// SUBJECTS JAVASCRIPT
new Vue({
	el: '#vue-container',
	data: {
		subjects: true,
		members: false,
		addform:false,
	},
	methods: {
		toggleSubjects: function () {
			this.subjects = true;
			this.addform = false;
			this.members = false;
		},
		toggleMembers: function () {
			this.members = this.members===true?false:true;
			this.subjects = false;
			this.addform = false;
		},
		addSubject:function(){
			this.addform = this.addform===true?false:true;
		},
	}
})
// SUBJECTS JAVASCRIPT

//EMPTY COMMENT ISSUE
new Vue({
	el:'#con',
	data:{
		comment:"",
	},
	computed:{
		disable:function(){
			if (this.comment.trim() == ""){
				return true
			}
		}
	}
})

//EMPTY COMMENT ISSUE ENDS

//HOMEPAGE JAVASCRIPT
var homepage = new Vue({
el:'#vuecontainer',
data:{
  joinform:false,
  createclassform:false,
},
methods:{
  create:function(){
    this.createclassform=true;
    this.joinform=false;
  },
  join:function(){
    this.createclassform=false;
    this.joinform=true;
  }
}
})
 //HOMEPAGE JAVASCRIPT ENDS

 // ASSIGNMENT PAGE JAVASCRIPT
 	new Vue({
		el:'#assignment-container',
		data:{
			all_submissions:true,
			ontime_submissions:false,
			late_submissions:false,
			submitted:false,
			not_submitted:true,
		},

		methods:{
			show_all_submissions:function(){
				this.all_submissions=true;
				this.ontime_submissions=false;
				this.late_submissions=false;
				this.submitted = false;
				this.not_submitted = false
			},

			show_ontime_submissions:function(){
				this.all_submissions=false,
				this.ontime_submissions=true,
				this.late_submissions=false;
				this.submitted = false;
				this.not_submitted = false
			},

			show_late_submissions:function(){
				this.all_submissions=false,
				this.ontime_submissions=false,
				this.late_submissions=true
				this.submitted = false;
				this.not_submitted = false
			},
			show_submitted:function(){
				this.all_submissions=false;
				this.ontime_submissions=false;
				this.late_submissions=false;
				this.submitted = true;
				this.not_submitted = false;
				console.log('submitted')
			},
			show_not_submitted:function(){
				this.all_submissions=false;
				this.ontime_submissions=false;
				this.late_submissions=false;
				this.submitted = false;
				this.not_submitted = true;
			},
		}
	})
 // ASSIGNMENT PAGE JAVASCRIPT ENDS 

 // PROFILE PAGE JS
 new Vue({
	el:'#profile',
	data:{
		updateForm:false,
	},
	methods:{
		showUpdateForm:function(){
			this.updateForm=this.updateForm===true?false:true;
		}
	}
})
// PROFILE PAGE JS ENDS

// POLL PAGE STARTS
new Vue({
	delimeters:['[[',']]'],
	el:'#poll-container',
	data:{
		message:'hello',
		p:4,
		form:false,
	},
	methods:{
		insert:function(){
			this.p = this.p+1
		},
		showform:function(){
			this.form = this.form===true?false:true;
		}
	}
})
// POLL PAGE ENDS 

	new Vue({
		el:'#update-form',
		data:{
			updateForm:false
		},
		methods:{
			classUpdateForm:function(){
				this.updateForm=this.updateForm===true?false:true;
				console.log('div')
			}
		}
	})