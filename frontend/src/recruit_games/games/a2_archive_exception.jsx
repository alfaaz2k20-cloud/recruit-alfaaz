import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function A2_ArchiveException({ onGameEnd, gameId }) {
    const [itemIdx, setItemIdx] = useState(0);
    const [flagged, setFlagged] = useState(false);
    const itemTimerRef = useRef(null);
    
    // Genuine exceptions: EXC_01, EXC_03, EXC_04. 
    // To fit 3 trials, use EXC_01, EXC_03, EXC_04. 
    const items = [
        { id: "EXC_01", label: "Hexagon" }, // genuine
        { id: "EXC_03", label: "Star" },    // genuine
        { id: "EXC_04", label: "Cross" }    // genuine
    ];

    useEffect(() => {
        if (itemIdx < items.length) {
            setFlagged(false);
            emit_event(gameId, items[itemIdx].id, 'item_presented', {}, { item_id: items[itemIdx].id });
            itemTimerRef.current = setTimeout(() => {
                handleDrop(null); // missed
            }, 5000);
        }
        return () => clearTimeout(itemTimerRef.current);
    }, [itemIdx]);

    const handleDrop = (bin) => {
        clearTimeout(itemTimerRef.current);
        const currentItem = items[itemIdx];
        if (bin) {
            emit_event(gameId, currentItem.id, 'item_dropped', {}, { item_id: currentItem.id, bin });
        }
        
        if (itemIdx < 2) {
            setItemIdx(i => i + 1);
        } else {
            onGameEnd();
        }
    };

    const toggleFlag = () => {
        setFlagged(!flagged);
        emit_event(gameId, items[itemIdx].id, 'flag_toggle', {}, { item_id: items[itemIdx].id });
    };

    if (itemIdx >= items.length) return null;
    const currentItem = items[itemIdx];

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>File each item. You can flag (?) exceptions.</p>
            
            <div style={{ padding: '20px', border: '1px solid black', marginBottom: '20px', position: 'relative' }}>
                <button 
                    onClick={toggleFlag} 
                    style={{ position: 'absolute', top: 5, right: 5, background: flagged ? 'red' : 'lightgray' }}
                >
                    ?
                </button>
                <strong>{currentItem.label}</strong>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-around' }}>
                <button onClick={() => handleDrop('A')}>Folder A</button>
                <button onClick={() => handleDrop('B')}>Folder B</button>
                <button onClick={() => handleDrop('C')}>Folder C</button>
            </div>
        </div>
    );
}
