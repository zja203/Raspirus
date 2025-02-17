import { useState, useContext, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { SettingsContext } from '../state/context';
import { useTranslation } from 'next-i18next';

export default function SettingComp({ title, short, short2 = null, icon, isOn: initialIsOn, action = null, action_val = null }) {
    const titleWithoutSpaces = title.replace(/ /g, "");
    const { settings, setSettings } = useContext(SettingsContext);
    const [isOn, setIsOn] = useState(initialIsOn || settings[titleWithoutSpaces]);
    const t = useTranslation('common').t;

    useEffect(() => {
        setSettings((prev) => ({ ...prev, [titleWithoutSpaces]: isOn }));
    }, [isOn, titleWithoutSpaces, setSettings])

    return (
        <div className="flex flex-col m-6 p-2 bg-white rounded-2xl shadow-md">
            <div className="flex items-center justify-between mx-4">
                <div className="flex items-center">
                    <FontAwesomeIcon
                        icon={icon}
                        size="2x"
                        className="w-16 h-16 rounded-2xl p-3 border border-maingreen-light text-maingreen-light bg-green-50"
                    />
                    <div className="flex flex-col ml-3">
                        <div className="font-medium leading-none">{title}</div>
                        <p className="text-sm text-gray-600 leading-none mt-1">{short}</p>
                        {short2 && <p className="text-sm text-gray-600 leading-none mt-1">{short2}</p>}
                    </div>
                </div>
                {action == null && 
                    <button onClick={() => setIsOn(!isOn)}
                    className={`flex-no-shrink px-5 ml-4 py-2 text-sm shadow-sm hover:shadow-lg font-medium tracking-wider border-2 text-white rounded-full ${isOn ? 'bg-green-500 border-green-500' : 'bg-red-500 border-red-500'}`}>
                    {isOn ? t('settings_on') : t('settings_off')}
                </button>
                }

                {action != null &&
                    <button onClick={action}
                    className={'flex-no-shrink px-5 ml-4 py-2 text-sm shadow-sm hover:shadow-lg font-medium tracking-wider border-2 text-white rounded-full bg-blue-500 border-blue-500'}>
                    {action_val}
                  </button>
                }
            </div>
        </div>
    );
}