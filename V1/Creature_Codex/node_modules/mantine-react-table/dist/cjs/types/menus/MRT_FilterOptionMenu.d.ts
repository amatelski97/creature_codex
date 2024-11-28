import { type MRT_Header, type MRT_InternalFilterOption, type MRT_Localization, type MRT_TableInstance } from '../types';
export declare const mrtFilterOptions: (localization: MRT_Localization) => MRT_InternalFilterOption[];
interface Props<TData extends Record<string, any> = {}> {
    header?: MRT_Header<TData>;
    onSelect?: () => void;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_FilterOptionMenu: <TData extends Record<string, any> = {}>({ header, onSelect, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
