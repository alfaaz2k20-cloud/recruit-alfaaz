import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function C1_CanvasSharing({ onGameEnd, gameId }) {
    const [section, setSection] = useState(1);
    const [playerPaint, setPlayerPaint] = useState(50);
    const [partnerPaint, setPartnerPaint] = useState(0); // For simulation visualization
    const [showShare, setShowShare] = useState(false);
    const [shareAmount, setShareAmount] = useState(1);
    
    const sections = [
        { id: 1, deficit: 5 },
        { id: 2, deficit: 15 }
    ];

    useEffect(() => {
        if (section > 2) return;
        const currentSection = sections[section - 1];
        
        emit_event(gameId, section.toString(), 'section_start', {}, { deficit: currentSection.deficit });
        setPlayerPaint(50);
        setShowShare(false);
        setShareAmount(1);
        
        // Partner simulation logic
        let partnerPaintLocal = 50 - currentSection.deficit; 
        setPartnerPaint(partnerPaintLocal);
        
        const paintInterval = setInterval(() => {
            setPartnerPaint(p => Math.max(0, p - 2));
        }, 1000);
        
        // Need/Request state
        const needTimeout = setTimeout(() => {
            emit_event(gameId, section.toString(), 'partner_state', {}, { state: 'NEED' });
        }, 3000);
        
        const sectionTimeout = setTimeout(() => {
            clearInterval(paintInterval);
            emit_event(gameId, section.toString(), 'section_end', {}, {});
            if (section < 2) {
                setSection(s => s + 1);
            } else {
                onGameEnd();
            }
        }, 10000);
        
        return () => {
            clearInterval(paintInterval);
            clearTimeout(needTimeout);
            clearTimeout(sectionTimeout);
        };
    }, [section]);

    const handleSend = () => {
        emit_event(gameId, section.toString(), 'share_send', {}, { amount: shareAmount });
        setPlayerPaint(p => Math.max(0, p - shareAmount));
        setShowShare(false);
    };

    if (section > 2) return null;

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>Paint your half. You can send paint to your partner.</p>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                <div>
                    <strong>You</strong>
                    <div>Paint: {playerPaint}</div>
                </div>
                <div>
                    <strong>Partner</strong>
                    <div>Paint: {partnerPaint}</div>
                </div>
            </div>
            
            {!showShare ? (
                <button onClick={() => {
                    setShowShare(true);
                    emit_event(gameId, section.toString(), 'share_open', {}, {});
                }}>Send paint</button>
            ) : (
                <div>
                    <input 
                        type="number" min="1" max="20" value={shareAmount}
                        onChange={e => setShareAmount(parseInt(e.target.value, 10) || 1)}
                    />
                    <button onClick={handleSend}>Send</button>
                </div>
            )}
            
            <div style={{ marginTop: '20px' }} 
                 onMouseDown={() => emit_event(gameId, section.toString(), 'paint_start', {}, {})}
                 onMouseUp={() => emit_event(gameId, section.toString(), 'paint_stop', {}, {})}>
                <button style={{ padding: '20px', width: '100%' }}>Hold to Paint</button>
            </div>
        </div>
    );
}
