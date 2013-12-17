function addToken() {
	var params = "token=" + document.getElementById("token").value;
	params = params + "&user=" + document.getElementById("user").value;
	params = params + "&email=" + document.getElementById("email").value;
	$.ajax({
		url: "/add/token",
		data: params,
		type: "POST"
	}).done(function(data) {
		showTokens();
	});
}

function tableHeader(items) {
	var row = document.createElement("tr");
	for (i=0; i<items.length; i++) {
		var cell = document.createElement('th');
		var txtCell = document.createTextNode(items[i]);
		cell.appendChild(txtCell);
		row.appendChild(cell);
	}
	return(row);
}

function showTokens() {
	var tb_token = document.getElementById('tb_token');
	var tbHeader = document.createElement("thead");
	tbHeader.id = "tk_thead";
	var tbBody = document.createElement("tbody");
	tbBody.id = "tk_tbody";
	tbHeader.appendChild(tableHeader(["Token","User","e-mail","Last Login","Action"]));
   	$.getJSON('/get/token', function(tokens) {
   		for (i=0,len=tokens.length;i<len;i++) {
			var row = document.createElement('tr');
			var cell = document.createElement('td');
			var txtCell = document.createTextNode(tokens[i].token);
			cell.appendChild(txtCell);
			row.appendChild(cell);
			var cell = document.createElement('td');
			var txtCell = document.createTextNode(tokens[i].user);
			cell.appendChild(txtCell);
			row.appendChild(cell);
			var cell = document.createElement('td');
			var txtCell = document.createTextNode(tokens[i].email);
			cell.appendChild(txtCell);
			row.appendChild(cell);
			var cell = document.createElement('td');
			var txtCell = document.createTextNode(tokens[i].lastlogin);
			cell.appendChild(txtCell);
			row.appendChild(cell);
			var cell = document.createElement('td');
			cell.innerHTML = "<input type='button' value='Email Token' onclick='emailToken(\"" + tokens[i].key +"\")'>";
			row.appendChild(cell);
   			tbBody.appendChild(row);
    	}
   	});
    tb_token.replaceChild(tbHeader, tk_thead);
    tb_token.replaceChild(tbBody, tk_tbody);
}

function showSessions() {
	var tb_sess = document.getElementById('tb_sess');
	var tbHeader = document.createElement("thead");
	tbHeader.id = "sess_thead";
	var tbBody = document.createElement("tbody");
	tbBody.id = "sess_tbody";
	tbHeader.appendChild(tableHeader(["User","Start Time"]));
   	$.getJSON('/get/session', function(session) {
   		for (i=0,len=session.length;i<len;i++) {
			var row = document.createElement('tr');
			var cell = document.createElement('td');
			var txtCell = document.createTextNode(session[i].user);
			cell.appendChild(txtCell);
			row.appendChild(cell);
			var cell = document.createElement('td');
			var txtCell = document.createTextNode(session[i].start);
			cell.appendChild(txtCell);
			row.appendChild(cell);
   			tbBody.appendChild(row);
    	}
   	});
    tb_sess.replaceChild(tbHeader, sess_thead);
    tb_sess.replaceChild(tbBody, sess_tbody);
}

function emailToken(token) {
	var params = "token=" + token;
	$.ajax({
		url: "/add/email_token",
		data: params,
		type: "POST"
	}).done(function(data) {
		alert(data)
	});
}
