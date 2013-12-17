var DeviceTypes = {};
var FeatureCategories = {};
var Features = {};
var Devices = {};

function post_to_url(path, params) {
	postreq = new XMLHttpRequest();
	postreq.open("POST", path, false);
	postreq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	postreq.send(params);
	return(postreq.responseText);
}

function setDTCookie(dt) {
	document.cookie="device_type=" + dt;
}

function getDTCookie() {
	var docCookies=document.cookie.split("; ");
	for (var i=0;i<docCookies.length;i++) {
		c = docCookies[i].split("=");
		if (c[0] == "device_type") {
			filt_dt = document.getElementById('filter_device_type')
			filt_dt.value = c[1]
			changeFilter(filt_dt)
		}
	}
}

function addDeviceType() {
	var params = "name=" + document.getElementById("device_type").value;
	params = params + "&key=" + document.getElementById("device_type_key").value;
	$('#dt_status').html(post_to_url("/add/device_type", params));
	$('#device_type').val('');
	$('#device_type_key').val('');
	loadDeviceTypes();
}

function loadDeviceTypes() {
	$.ajax({ url: '/get/device_type', dataType: 'json', async: false }).done(function(dv_types) {
    	DeviceTypes = dv_types;
    });
}

function optDeviceTypes(select, selected) {
	select.options.length = 0;
	opt = new Option("Select a Device Type");
	opt.value = "";
	select.options[0] = opt;
	for (var i=0,len=DeviceTypes.length;i<len;i++) {
		opt = new Option(DeviceTypes[i].name, DeviceTypes[i].key);
		if (selected == DeviceTypes[i].key) opt.selected = true;
		select.options[i+1] = opt;
	}
}

function updateTbDeviceTypes() {
   	$('#tbDeviceTypes tbody > tr').remove();
    for (var i=0,len=DeviceTypes.length;i<len;i++) {
    	$("#tbDeviceTypes tbody")
        .append($('<tr>')
        	.append($('<td>')
                .append(DeviceTypes[i].name)
            ).append($('<td>')
                .append("<input type='button' value='Edit' onclick='editDeviceType(\"" + DeviceTypes[i].key +"\")'>")
            )
        );
    $('#tbDeviceTypes').trigger('update');
    }
}

function editDeviceType(device_type_key) {
	for (var i=0,len=DeviceTypes.length;i<len;i++) {
		if (DeviceTypes[i].key == device_type_key) {
			$('#device_type').val(DeviceTypes[i].name);
			$('#device_type_key').val(DeviceTypes[i].key);
			$('#dt_status').html('');
   			break;
		}
	}
}

function addFeatureCategory() {
	var params = "name_eng=" + document.getElementById("fc_name_eng").value;
	params = params + "&key=" + document.getElementById("fc_key").value;
	params = params + "&name_spa=" + document.getElementById("fc_name_spa").value;
	params = params + "&name_por=" + document.getElementById("fc_name_por").value;
	params = params + "&dv_type=" + document.getElementById("fc_device_type").value;
	$('#fc_status').html(post_to_url("/add/feature_category", params));
	$('#fc_name_eng').val('');
	$('#fc_key').val('');
	$('#fc_name_spa').val('');
	$('#fc_name_por').val('');
	loadFeatureCategories();
}

function loadFeatureCategories() {
	filter_dt = $('#filter_device_type').val();
	url = '/get/feature_category';
	if (filter_dt != '') url += '?device_type=' + filter_dt;
	$.ajax({ url: url, dataType: 'json', async: false }).done(function(fc) {
    	FeatureCategories = fc;
    });
}

function optFeatureCategories(select, selected) {
	select.options.length = 0;
	opt = new Option("Select a Feature Category");
	opt.value = "";
	select.options[0] = opt;
	for (var i=0,len=FeatureCategories.length;i<len;i++) {
		opt = new Option(FeatureCategories[i].name_eng, FeatureCategories[i].key);
		if (selected == FeatureCategories[i].key) opt.selected = true;
		select.options[i+1] = opt;
   	}
}

function updateTbFeatureCategories() {
	$('#tbFeatureCategories tbody > tr').remove();
	for (var i=0,len=FeatureCategories.length;i<len;i++) {
		$("#tbFeatureCategories tbody")
		.append($('<tr>')
			.append($('<td>')
				.append(FeatureCategories[i].device_type_name)
			).append($('<td>')
				.append(FeatureCategories[i].name_eng)
			).append($('<td>')
				.append(FeatureCategories[i].name_spa)
			).append($('<td>')
				.append(FeatureCategories[i].name_por)
			).append($('<td>')
				.append("<input type='button' value='Edit' onclick='editFeatureCategory(\"" + FeatureCategories[i].key +"\")'>")
			)
		);
		$('#tbFeatureCategories').trigger('update');
	}
}

function editFeatureCategory(fc_key) {
	in_fc_dev_type = document.getElementById('fc_device_type');
	for (var i=0,len=FeatureCategories.length;i<len;i++) {
		if (FeatureCategories[i].key == fc_key) {
			$('#fc_name_eng').val(FeatureCategories[i].name_eng);
			$('#fc_key').val(FeatureCategories[i].key);
			optDeviceTypes(in_fc_dev_type, FeatureCategories[i].device_type_key);
			$('#fc_name_spa').val(FeatureCategories[i].name_spa);
			$('#fc_name_por').val(FeatureCategories[i].name_por);
			$('#fc_status').html('');
   			break;
		}
	}
}

function addFeature() {
	var params = "name=" + $('#feat_name').val();
	params = params + "&key=" + $('#feat_key').val();
	params = params + "&category=" + $('#feat_category').val();
	params = params + "&desc_eng=" + $('#desc_eng').val();
	params = params + "&desc_spa=" + $('#desc_spa').val();
	params = params + "&desc_por=" + $('#desc_por').val();
	$('#feat_status').html(post_to_url("/add/feature", params));
	$('#feat_name').val('');
	$('#feat_key').val('');
	$('#desc_eng').val('');
	$('#desc_spa').val('');
	$('#desc_por').val('');
	loadFeatures();
}

function loadFeatures() {
	filter_dt = $('#filter_device_type').val();
	filter_fc = $('#filter_feature_category').val();
	url = '/get/feature';
	if (filter_dt != '') url += '?device_type=' + filter_dt;
	if (filter_fc != '') url += '&feature_category=' + filter_fc;
	$.ajax({ url: url, dataType: 'json', async: false }).done(function(feats) {
    	Features = feats;
    });
}

function updateTbFeatures() {
	$('#tbFeatures tbody > tr').remove();
	for (i=0,len=Features.length;i<len;i++) {
		$("#tbFeatures tbody")
		.append($('<tr>')
			.append($('<td>')
				.append(Features[i].category_name)
			).append($('<td>')
				.append(Features[i].name)
			).append($('<td>')
				.append(Features[i].desc_eng)
			).append($('<td>')
				.append(Features[i].desc_spa)
			).append($('<td>')
				.append(Features[i].desc_por)
			).append($('<td>')
				.append("<input type='button' value='Edit' onclick='editFeatures(\"" + Features[i].key +"\")'>")
			)
		);
		$('#tbFeatures').trigger('update');
	}
}

function editFeatures(feat_key) {
	in_feat_dev_type = document.getElementById('feat_device_type');
	in_feat_category = document.getElementById('feat_category');
	$.ajax({ url: '/get/feature?key='+feat_key, dataType: 'json', async: false }).done(function(feat) {
		$('#feat_name').val(feat[0].name);
		$('#feat_key').val(feat[0].key);
		optDeviceTypes(in_feat_dev_type, feat[0].device_type_key);
		optFeatureCategories(in_feat_category, feat[0].category_key);
		$('#desc_eng').val(feat[0].desc_eng);
		$('#desc_spa').val(feat[0].desc_spa);
		$('#desc_por').val(feat[0].desc_por);
		$('#feat_status').html('');
	});
}

function addDevice() {
	var params = "vendor=" + $('#dev_vendor').val();
	params = params + "&key=" + $('#dev_key').val();
	params = params + "&model=" + $('#dev_model').val();
	params = params + "&description=" + $('#dev_desc').val();
	params = params + "&device_type=" + $('#dev_device_type').val();
	$('#dev_status').html(post_to_url("/add/device", params));
	$('#dev_vendor').val('');
	$('#dev_key').val('');
	$('#dev_model').val('');
	$('#dev_desc').val('');
	loadDevices();
}

function loadDevices() {
	filter_dt = $('#filter_device_type').val();
	url = '/get/device';
	if (filter_dt != '') url += '?device_type=' + filter_dt;
	$.ajax({ url: url, dataType: 'json', async: false }).done(function(devs) {
    	Devices = devs;
    });
}

function updateTbDevices() {
	$('#tbDevices tbody > tr').remove();
	for (var i=0,len=Devices.length;i<len;i++) {
		$("#tbDevices tbody")
		.append($('<tr>')
			.append($('<td>')
				.append(Devices[i].device_type_name)
			).append($('<td>')
				.append(Devices[i].vendor)
			).append($('<td>')
				.append(Devices[i].model)
			).append($('<td>')
				.append(Devices[i].description)
			).append($('<td>')
				.append("<input type='button' value='Edit' onclick='editDevices(\"" + Devices[i].key +"\");'>")
			)
		);
		$('#tbDevices').trigger('update');
	}
}

function editDevices(dev_key) {
	in_dev_dev_type = document.getElementById('dev_device_type');
	$.getJSON('/get/device?key='+dev_key, function(dev) {
		$('#dev_vendor').val(dev[0].vendor);
		$('#dev_model').val(dev[0].model);
		$('#dev_key').val(dev[0].key);
		optDeviceTypes(in_dev_dev_type, dev[0].device_type_key);
		$('#dev_desc').val(dev[0].description);
		$('#dev_status').html('');
	});
}

