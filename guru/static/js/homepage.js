if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

function openNav() {
    document.getElementById("mySidenav").style.width = "295px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function createclassform() {
    if (document.getElementById('classform').style.display == 'none') {
        document.getElementById('joinform').style.display = 'none';
        document.getElementById('classform').style.display = 'block';
    } else {
        document.getElementById('classform').style.display = 'none'
    }
}

function joinform() {
    if (display == document.getElementById('joinform').style.display == 'none') {
        document.getElementById('classform').style.display = 'none'
        document.getElementById('joinform').style.display = 'block';
    } else {
        document.getElementById('joinform').style.display = 'none';
    }
}

// POLL JS
function addInputField(){
    document.getElementById('more-inputs').innerHTML += '<input type="text" autocomplete="off" class="new" placeholder="Mention your option..." name="check">'
    new_inputs = document.getElementsByClassName('new')
    new_inputs[new_inputs.length-1].focus()

}

function toggleFlexForm(x){
    x.style.display=x.style.display=='none'?'flex':'none';
}

function toggleBlockForm(x){
    if (!x.style.display || x.style.display == "none") {
        x.style.display = "block";
    }
    else {
        x.style.display = "none";
    }
}  

//EMPTY COMMENT ISSUE
function checkComment(){
    var value=document.getElementById('id_comment').value
    value = value.trim()
    if(value.length==0){
        document.getElementById('id_submit').disabled=true;
    }
    else{
        document.getElementById('id_submit').disabled=false;
    }
}

//EMPTY COMMENT ISSUE ENDS

//HOMEPAGE JAVASCRIPT
function on() {
    document.getElementById("overlay").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
}
//HOMEPAGE JAVASCRIPT ENDS

// SUBJECTS JAVASCRIPT
new Vue({
        el: '#vue-container',
        data: {
            subjects: true,
            members: false,
            addform: false,
        },
        methods: {
            toggleSubjects: function() {
                this.subjects = true;
                this.addform = false;
                this.members = false;
            },
            toggleMembers: function() {
                this.members = this.members === true ? false : true;
                this.subjects = false;
                this.addform = false;
            },
            addSubject: function() {
                this.addform = this.addform === true ? false : true;
            },
        }
    })
// SUBJECTS JAVASCRIPT

// ASSIGNMENT PAGE JAVASCRIPT
new Vue({
    el: '#assignment-container',
    data: {
        all_submissions: false,
        ontime_submissions: false,
        late_submissions: false,
        not_submitted: false,
        clear: true,
    },

    methods: {
        cleared: function() {
            this.all_submissions = false;
            this.ontime_submissions = false;
            this.late_submissions = false;
            this.not_submitted = false;
            this.clear = true
        },
        show_all_submissions: function() {
            this.all_submissions = true;
            this.ontime_submissions = false;
            this.late_submissions = false;
            this.not_submitted = false
        },

        show_ontime_submissions: function() {
            this.all_submissions = false,
                this.ontime_submissions = true,
                this.late_submissions = false;
            this.not_submitted = false
        },

        show_late_submissions: function() {
            this.all_submissions = false,
                this.ontime_submissions = false,
                this.late_submissions = true
            this.not_submitted = false
        },
        show_not_submitted: function() {
            this.all_submissions = false;
            this.ontime_submissions = false;
            this.late_submissions = false;
            this.not_submitted = true;
        },
    }
})
// ASSIGNMENT PAGE JAVASCRIPT ENDS 

// This subject JS
new Vue({
    el: '#subject',
    data: {
        'members': true,
        'activity': false,
        'editForm': false,
    },
    methods: {
        toggleMembers: function() {
            this.members = true;
            this.activity = false;
            this.editform = false;
        },
        toggleActivity: function() {
            this.members = false;
            this.editform = false;
            this.activity = true;
        },
        toggleEditForm: function() {
            this.editForm = this.editForm === true ? false : true;
        }
    }
})