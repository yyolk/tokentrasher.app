// via https://github.com/XRPL-Labs/offer-create-xapp/blob/ff41d819614b03b788d38c13bf261a9d7ee1afd5/src/plugins/rippled-vue.js
// Authored-by: KoenPaas <koen@paas.nl>
//
import { XrplClient } from 'xrpl-client'

let ws = null

export default {
    // install: (app, options) => {
    install: (app) => {
        const connect = async (url, options) => {
            if (ws != null) return ws
            ws = new XrplClient(url, options)
            // ws = await connection.ready()
            return ws
        }

        const getState = () => {
            return ws.getState()
        }

        const close = () => {
            ws.close().then(closeInfo => {
                console.log('Closed', closeInfo)
            }).catch(error => {
                console.log('Close error', error)
            })
        }

        const send = async (command) => {
            const response = await ws.send(command)
            return response
        }

        const on = (event, fn) => {
            ws.on(event, fn)
        }

        app.config.globalProperties.$rippled = {
            connect,
            getState,
            close,
            send,
            on
        }
    }
}
