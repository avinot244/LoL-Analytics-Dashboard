
import Select from 'react-select';
import "../styles/SelectComp.css"
import { useState } from 'react';

function SearchComp({selectedElement, setSelectedElement, elementList}) {

	return (	
		<>
			<Select
				className="searchComp"
				classNamePrefix="select"
				isClearable={true}
				isSearchable={true}
				options={elementList}
				onChange={(element) => setSelectedElement(element.value)}
				
			/>
		</>
	);
}

export default SearchComp;
