/*!
 * Joel Brigida
 * JS Code for Calculations
*/

function calculate()
{
	//alert("CALL TO CALCULATE FUNCTION"); 									// DEBUG
	let userEntry = document.getElementById("userInput").value;				// read all values entered by the user
	let arrayUserNum = userEntry.split(",").map(Number); 					// map all numbers into an array 

	let validEntry;															// define a variable to verify the user input
	for (let currentElement of arrayUserNum)								// iterate elements of array to look for any NaN values
	{
		if (Number.isNaN(currentElement))
		{
			validEntry = 0;													// represents invalid user entry
		}
		else
		{
			validEntry = 1;													// proper input: continue calculation
		}
	}
	
	let theMin = document.getElementById("minOutput");						// define variable which will become the minimum
	let theMax = document.getElementById("maxOutput");						// define variable which will become the maximum
	let theMean = document.getElementById("meanOutput");					// define variable which will become the mean
	let theMedian = document.getElementById("medianOutput");				// define variable which will become the median
	let theRange = document.getElementById("rangeOutput");					// define variable which will become the Range

	if (validEntry == 0)													// if invalid entry: output error message to the boxes
	{
		theMin.value = theMax.value = theMean.value = theMedian.value = theRange.value = "Invalid Entry: Please Enter Only Numbers!";
	} 
	else																	// perform calculations if entries are valid
	{ 
		// sort() source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort	
		arrayUserNum.sort((a,b) => a-b);									// sorts array in order
		
		theMax.value = maximum(arrayUserNum);								// function call to maximum
		theMin.value = minimum(arrayUserNum);								// function call to minimum
		theMean.value = mean(arrayUserNum); 								// function call to mean
		theMedian.value = median(arrayUserNum);								// function call to median
		theRange.value = range(arrayUserNum);								// function call to range
	}
}	// END of Calculate Function

/** Begin Sub-Functions for Calculator */

function maximum(arrayUserNum)
{
	// Math.max() source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/max
	//alert("CALL TO MAXIMUM FUNCTION");
	return Math.max(...arrayUserNum); 										// find maximum in array
}

function minimum(arrayUserNum)
{
	// Math.min() source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/min
	//alert("CALL TO MINIMUM FUNCTION");
	return Math.min(...arrayUserNum);										// find minimum in array
}

function mean(arrayUserNum)
{ 
	// reduce() method source: https://stackoverflow.com/questions/1230233/how-to-find-the-sum-of-an-array-of-numbers
	//alert("CALL TO MEAN FUNCTION");
	let totalValue = arrayUserNum.reduce((a,b) => a + b, 0);				// calculate total value of array indices
	return (totalValue / arrayUserNum.length);								// return the average of all indices
}

function median(arrayUserNum)
{

	// median function source: https://stackoverflow.com/questions/45309447/calculating-median-javascript/45309555#45309555
	// Math.floor() source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/floor
	//alert("CALL TO MEDIAN FUNCTION");										// DEBUG
	let middleValue = Math.floor(arrayUserNum.length / 2);
	
	arrayUserNum.sort(function(a,b) {										// reverse sort the array, otherwise
		return (a - b);														// even # of array indices will show incorrect median
	});
	
	if (arrayUserNum.length % 2 == 1) 										// odd number of indices: display middle value
	{
		return arrayUserNum[middleValue];
	} 
	else 																	// average 2 middle values if there is an even number of indices
	{ 
		return (arrayUserNum[middleValue - 1] + arrayUserNum[middleValue]) / 2;				
	}
}

function range(arrayUserNum)
{
	//alert("CALL TO RANGE FUNCTION");										// DEBUG
	return arrayUserNum[arrayUserNum.length - 1] - arrayUserNum[0];			// last index - 1st index = range
}
