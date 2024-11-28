import { type MRT_TableInstance, type MRT_VirtualItem } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    table: MRT_TableInstance<TData>;
    virtualColumns?: MRT_VirtualItem[];
    virtualPaddingLeft?: number;
    virtualPaddingRight?: number;
}
export declare const MRT_TableHead: <TData extends Record<string, any> = {}>({ table, virtualColumns, virtualPaddingLeft, virtualPaddingRight, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
