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

//EMPTY COMMENT ISSUE
new Vue({
    el: '#con',
    data: {
        comment: "",
    },
    computed: {
        disable: function() {
            if (this.comment.trim() == "") {
                return true
            }
        }
    }
})

//EMPTY COMMENT ISSUE ENDS

//HOMEPAGE JAVASCRIPT
var homepage = new Vue({
    el: '#vuecontainer',
    data: {
        joinform: false,
    },
    methods: {
        join: function() {
            this.joinform = this.joinform === true ? false : true;
        }
    }
})

function on() {
    document.getElementById("overlay").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
}
//HOMEPAGE JAVASCRIPT ENDS

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

new Vue({
        el: '#containassignment',
        data: {
            addform: false,
        },
        methods: {
            addAssignmentFormToggle: function() {
                this.addform = this.addform === true ? false : true;
            }
        }
    })
    // ASSIGNMENT PAGE JAVASCRIPT ENDS 

// PROFILE PAGE JS
new Vue({
        el: '#profile',
        data: {
            updateForm: false,
        },
        methods: {
            showUpdateForm: function() {
                this.updateForm = this.updateForm === true ? false : true;
            }
        }
    })
    // PROFILE PAGE JS ENDS

// POLL PAGE STARTS
new Vue({
        delimeters: ['[[', ']]'],
        el: '#poll-container',
        data: {
            message: 'hello',
            p: 4,
            form: false,
        },
        methods: {
            insert: function() {
                this.p = this.p + 1
            },
            showform: function() {
                this.form = this.form === true ? false : true;
            }
        }
    })
    // POLL PAGE ENDS 

new Vue({
    el: '#update-form',
    data: {
        updateForm: false
    },
    methods: {
        classUpdateForm: function() {
            this.updateForm = this.updateForm === true ? false : true;
        }
    }
})

// Announcement page JS
new Vue({
    el: '#containannouncement',
    data: {
        addform: false,
    },
    methods: {
        addAnnouncementFormToggle: function() {
            this.addform = this.addform === true ? false : true;
        }
    }
})

new Vue({
        el: '#contain',
        data: {
            updateform: false,
        },
        methods: {
            updateFormToggle: function() {
                this.updateform = this.updateform === true ? false : true;
            }
        }
    })
    // Anouncement page JS ends

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

// This subject JS ends

// Resources JS
new Vue({
    el: '#resource-contain',
    data: {
        addform: false,
    },
    methods: {
        addFormToggle: function() {
            this.addform = this.addform === true ? false : true;
        }
    }
})
new Vue({
        el: '#note-contain',
        data: {
            showUpdateForm: false,
        },
        methods: {
            formToggle: function() {
                this.showUpdateForm = this.showUpdateForm === true ? false : true;
            }
        }
    })
    // Resource page ends