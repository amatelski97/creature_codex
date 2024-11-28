import { type ReactNode } from 'react';
import { type MRT_Cell, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    cell: MRT_Cell<TData>;
    children: ReactNode;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_CopyButton: <TData extends Record<string, any> = {}>({ cell, children, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
