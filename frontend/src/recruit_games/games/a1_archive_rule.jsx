import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function A1_ArchiveRule({ onGameEnd, gameId }) {
    const [itemIdx, setItemIdx] = useState(0);
    const [showRules, setShowRules] = useState(false);
    const itemTimerRef = useRef(null);
    
    const items = [
        { id: "item1", label: "Dotted", correct: "A" },
        { id: "item2", label: "Squares", correct: "B" },
        { id: "item3", label: "Striped", correct: "C" }
    ];

    useEffect(() => {
        if (itemIdx < items.length && !showRules) {
            emit_event(gameId, items[itemIdx].id, 'item_presented', {}, { item_id: items[itemIdx].id });
            itemTimerRef.current = setTimeout(() => {
                handleDrop(null); // missed
            }, 5000);
        }
        return () => clearTimeout(itemTimerRef.current);
    }, [itemIdx, showRules]);

    const handleDrop = (bin) => {
        clearTimeout(itemTimerRef.current);
        const currentItem = items[itemIdx];
        if (bin) {
            const isCorrect = bin === currentItem.correct;
            emit_event(gameId, currentItem.id, 'item_dropped', {}, { item_id: currentItem.id, bin, correct: isCorrect });
            if (isCorrect) {
                emit_event(gameId, currentItem.id, 'item_correct', {}, { item_id: currentItem.id });
            }
        }
        
        if (itemIdx < 2) {
            setItemIdx(i => i + 1);
        } else {
            onGameEnd();
        }
    };

    const toggleRules = () => {
        if (showRules) {
            emit_event(gameId, items[itemIdx]?.id || 'none', 'rules_close', {}, {});
            setShowRules(false);
        } else {
            clearTimeout(itemTimerRef.current); // Pause timer while reading rules
            emit_event(gameId, items[itemIdx]?.id || 'none', 'rules_open', {}, {});
            setShowRules(true);
        }
    };

    if (showRules) {
        return (
            <div style={{ textAlign: 'center' }}>
                <p>Rules: Dotted → A. Striped → C. Circles → A. Squares → B. Triangles → C.</p>
                <button onClick={toggleRules}>Close Rules</button>
            </div>
        );
    }

    if (itemIdx >= items.length) return null;

    const currentItem = items[itemIdx];

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>File each item into the correct folder.</p>
            <button onClick={toggleRules} style={{ marginBottom: '20px' }}>Rules</button>
            
            <div style={{ padding: '20px', border: '1px solid black', marginBottom: '20px' }}>
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
