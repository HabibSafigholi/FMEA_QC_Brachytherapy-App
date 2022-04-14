// creat new task 
    "use strict";
	
	function newTask(event) {
		// clearing the form fields
		document.querySelector("[name='title']").value = "";
		document.querySelector("[name='due']").value = "";
		document.querySelector("[name='category']").value = "";
		document.querySelector("[name='Potentail_failure_mode']").value = "";
		document.querySelector("[name='Potentail_cause_failure']").value = "";
		document.querySelector("[name='Potentail_effects_failure']").value = "";
		document.querySelector("[name='Occurrence']").value = "";
		document.querySelector("[name='Severity']").value = "";
		document.querySelector("[name='Detect']").value = "";
		document.querySelector("[name='RPN']").value = "";
		document.querySelector("[name='notes']").value = "";		
		document.querySelector("[name='status']").value = "";
		document.querySelector("[name='id']").value = "";
		document.querySelector("[name='title']").value = "";
		
		
	}

	function newFolder(event) {
	    let name = prompt ("Name of new folder?")	
		let userid = document.querySelector ("[name='userid']").value;
		if (name.length > 0) {
		    let f = new FormData();
	        f.append("userid", userid);
	        f.append("name", name);
	        fetch("/new_folder", {
		        "method" : "POST" ,
		        "body": f,
	        }).then(response => response.text()).then(data => {
                console.log	("newFolder reply: ", data);
		        location.reload();
	        });	
	    }
	}

	document.querySelector("#new_task_button").addEventListener("click", newTask); 
	document.querySelector("#new_folder_button").addEventListener("click", newFolder);