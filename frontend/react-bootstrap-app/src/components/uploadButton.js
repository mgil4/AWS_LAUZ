import React, { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


const UploadButton = ({ onClick }) => {
    return (
        <Button variant="primary" size="lg" onClick={onClick}>
            Displays ratings
        </Button>
    );
};
export default UploadButton;