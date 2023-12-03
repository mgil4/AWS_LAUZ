import React, { useState } from 'react';
import UploadButton from './uploadButton.js';
import Scatter3D  from './plot.js';
import {backendGET} from "../controllers/backendCommunication"

const MyForm = () => {
    const [inputValue, setInputValue] = useState('');
    const [data, setData] = useState(null);


    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };
    const handleButtonClick = () => {
        if (inputValue === ''){
            alert('You cannot send an empty value');
        } else {
            backendGET("http://127.0.0.1:5000/api/data/?name="+inputValue).then((data) => {
                setData(data);
            });
        }
    };

    return (
        <div className="p-3">
            <div>
            <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                placeholder="Enter a mobile phone model"
                className="mobile-input mr-3"
            />
            <UploadButton onClick={handleButtonClick}/>
            </div>
            <br/>
            {data !== null && <Scatter3D productInfo={data} />}
        </div>

    );
};

export default MyForm;