import Form from 'react-bootstrap/Form';

function SelectComp({elementList, defaultValue}) {
	return (
		<Form.Select aria-label="Default select example">
			<option>{defaultValue}</option>
			{elementList.map((element) => (
				<option value={element}>{element}</option>
			))}
		</Form.Select>
	);
}

export default SelectComp;