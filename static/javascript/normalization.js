const minimum_division = document.getElementById("minimum_division");
const maximum_division = document.getElementById("maximum_division");

const normalization = document.getElementById("normalization");

normalization.onchange = (event) => {
	let method = event.target.value;

	if (method == "minmax") {
		minimum_division.classList.remove("hidden");
		maximum_division.classList.remove("hidden");
	}

	if (method == "zscore") {
		minimum_division.classList.add("hidden");
		maximum_division.classList.add("hidden");
	}
};
