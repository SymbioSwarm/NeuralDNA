// This is a simplistic web scraper designed specifically for the page
// http://www.ncbi.nlm.nih.gov/genome/browse/?report=5
// Please follow the steps exactly to download the .csv with all
// data included

//Set the selects to "Plants", "Land Plants", and "Cloroplast"
var total_arr = []

//Run the following for each page of results (You have to run it multiple times)
$('#project_list_organelles tbody tr').each(function(i,row){
	var $row=$(row);
	var arr = [];
	arr.push($row.children()[0].children[0].text) //Get name
	arr.push($row.children()[0].children[0].href) //URL
	arr.push($row.children()[6].innerHTML) //Size
	arr.push($row.children()[7].innerHTML) //GC
	arr.push($row.children()[9].innerHTML) //rRNA
	arr.push($row.children()[10].innerHTML) //tRNA
	arr.push($row.children()[12].innerHTML) //gene
	total_arr.push(arr)
})

//Run this when you are finished (Make sure pop up blocks are done)
var exportToCsv = function(total_arr) {
	var str = "Name,URL,Size,GC,rRNA,tRNA,gene";
	for (index = 0; index < total_arr.length; index++){
		str += "\n";
		var r = total_arr[index];
		for (j = 0; j < r.length; j++){
			str += r[j] + ",";
		}
		str = str.substring(0,str.length-1);
	}
	console.log(str);
	window.open('data:text/csv;charset=utf-8,' + escape(str));
	return str;
}
exportToCsv(total_arr);
