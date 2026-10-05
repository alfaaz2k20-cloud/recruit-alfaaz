import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function F2_FrequencyAmbiguous({ onGameEnd, gameId }) {
    const [round, setRound] = useState(1);
    const [sliderVal, setSliderVal] = useState(50);
    const [cue, setCue] = useState(null);
    const [showAsk, setShowAsk] = useState(false);
    
    const roundTimerRef = useRef(null);
    const cueTimerRef = useRef(null);
    const askTimerRef = useRef(null);
    
    const rounds = [
        { id: 1, peak: 90, comfort: 30, text: "Hmm..." },
        { id: 2, peak: 10, comfort: 80, text: "I don't know" }
    ];

    const currentRound = rounds[round - 1];

    useEffect(() => {
        if (!currentRound) return;
        
        emit_event(gameId, round.toString(), 'round_start', {}, { peak: currentRound.peak, comfort: currentRound.comfort });
        setSliderVal(50);
        setCue(null);
        setShowAsk(false);
        
        cueTimerRef.current = setTimeout(() => {
            setCue(currentRound.text);
            emit_event(gameId, round.toString(), 'cue_shown', {}, { text: currentRound.text });
        }, 2000);
        
        askTimerRef.current = setTimeout(() => {
            setShowAsk(true);
        }, 3000);
        
        roundTimerRef.current = setTimeout(() => {
            handleLockIn(sliderVal);
        }, 8000);
        
        return () => {
            clearTimeout(cueTimerRef.current);
            clearTimeout(askTimerRef.current);
            clearTimeout(roundTimerRef.current);
        };
    }, [round]);

    const handleLockIn = (val) => {
        clearTimeout(cueTimerRef.current);
        clearTimeout(askTimerRef.current);
        clearTimeout(roundTimerRef.current);
        emit_event(gameId, round.toString(), 'lock_in', {}, { x_final: val });
        emit_event(gameId, round.toString(), 'round_end', {}, {});
        if (round < 2) {
            setRound(r => r + 1);
        } else {
            onGameEnd();
        }
    };

    const handleAsk = () => {
        setShowAsk(false);
        emit_event(gameId, round.toString(), 'ask_press', {}, {});
        setCue(round === 1 ? "Lower it a lot." : "Raise it a bit."); // some response
    };

    if (!currentRound) return null;

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>Tune the channel. A producer is listening.</p>
            <div style={{ height: '40px' }}>{cue && <strong>{cue}</strong>}</div>
            <input 
                type="range" min="0" max="100" value={sliderVal} 
                onChange={(e) => {
                    const val = parseInt(e.target.value, 10);
                    setSliderVal(val);
                    emit_event(gameId, round.toString(), 'slider_change', {}, { value: val });
                }} 
                style={{ width: '100%', margin: '20px 0' }}
            />
            {showAsk && <button onClick={handleAsk} style={{ marginRight: '10px' }}>Ask</button>}
            <button onClick={() => handleLockIn(sliderVal)}>Lock in</button>
            <p>Round {round} of 2</p>
        </div>
    );
}
