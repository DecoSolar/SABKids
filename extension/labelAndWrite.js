let host = 'http://localhost:8000';

function api(endpoint, method, data) { // отправка изображений на проверку
	let xhr = new XMLHttpRequest();
	xhr.open(method, `${host}/${endpoint}`);
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4) {
			console.log(xhr.status);
			console.log(xhr.responseText);
			i = xhr.responseText;
			if (i == '{"message":"No images sent in request"}') {
				i = 1;
			}
			else if (xhr.status == 0) {
				i = 1;
			}
			showCover(i);
		}
	};
	xhr.send(JSON.stringify(data));
}

function apiForChekLink(endpoint, method, data) { // отправка ссылки на проверку
	let xhr = new XMLHttpRequest();
	xhr.open(method, `${host}/${endpoint}`);
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onload = function() {
		console.log(xhr.responseText);
		i = xhr.responseText;
		if (i == -1){
			return i;
		}
		else {
			showCover(i);
			return 'done';
		}
	};
	xhr.send(JSON.stringify(data));
	
}

function ready() {  // считывание ссылок на изображение, отправление их на сервер и проверка
	var links = [];
	for (var i = 0; i < document.images.length; i++) {
		links.push(document.images[i].src);
	}
	try {
		api('test', 'post', links);
	} catch (e) {
		console.log(e)
	}
}

function showCover(i) { // блокирока страницы и дальнейшее действие, после результата проверки
	if (i == 0) {
		document.body.style.display = 'none';// страница загружается однотонной
	}
	else if (i == 1) {
		document.body.style.display = 'block';// показать страницу, если прошла проверку
	}
	else if (i == 2) {
		location.replace("https://yandex.ru/");// перейти на яндекс, если не прошла
	}
}

function chekLinks() { // проверка ссылки на наличие в списке
	let currentLink = []
	if (document.location.href == 'https://yandex.ru/') {
		showCover(1);
		return 'done';
	}
	else {
		currentLink.push(document.location.href);
		running = apiForChekLink('links', 'post', currentLink);
		return running;
	}
}

let i = 0;
showCover(i);
chek = chekLinks();
if (chek == 'done') {
	console.log("Finish");
}
else {
	ready();
}